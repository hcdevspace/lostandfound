"""
Simple in-memory rate limiter for Django views.

Uses Django's cache framework (defaults to local-memory cache, which works
out of the box with no extra dependencies). If you later configure Redis or
Memcached as Django's cache backend, this will use that automatically.

Rate limits are keyed by (view name, IP address) so each user/IP gets their
own independent counter per endpoint.
"""

import functools
import time
from django.core.cache import cache
from django.http import HttpResponse


def _get_client_ip(request):
    """Extract the real client IP, respecting common proxy headers."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def rate_limit(max_requests: int, window_seconds: int, methods=("POST",)):
    """
    Decorator that enforces a sliding-window rate limit on a view.

    Args:
        max_requests:    Maximum number of allowed requests within the window.
        window_seconds:  Length of the rolling window in seconds.
        methods:         HTTP methods to apply the limit to (default: POST only).
                         Pass methods=None to limit all methods.

    When the limit is exceeded the view returns HTTP 429 with a plain-text
    message and a Retry-After header.
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Only throttle the specified HTTP methods
            if methods is not None and request.method not in methods:
                return view_func(request, *args, **kwargs)

            ip = _get_client_ip(request)
            cache_key = f"rl:{view_func.__name__}:{ip}"

            now = time.time()
            window_start = now - window_seconds

            # Retrieve the list of timestamps for previous requests
            timestamps = cache.get(cache_key, [])

            # Drop timestamps that fall outside the current window
            timestamps = [t for t in timestamps if t > window_start]

            if len(timestamps) >= max_requests:
                # Calculate how long until the oldest request ages out
                retry_after = int(timestamps[0] - window_start) + 1
                response = HttpResponse(
                    f"Too many requests. Please wait {retry_after} seconds before trying again.",
                    status=429,
                    content_type="text/plain",
                )
                response["Retry-After"] = retry_after
                return response

            # Record this request and persist with enough TTL to cover the window
            timestamps.append(now)
            cache.set(cache_key, timestamps, timeout=window_seconds + 5)

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator