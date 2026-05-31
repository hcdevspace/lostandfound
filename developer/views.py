import json
import os
import time
import secrets
from functools import wraps

from django.contrib import auth as django_auth
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone

from accounts.models import CustomUser
from items.models import Item
from claims.models import Claim

_relogin_tokens = {}
_TOKEN_EXPIRY = 7200


def admin_only(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'error': 'Forbidden'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapped


@admin_only
@require_GET
def snapshot(request):
    items_data = []
    for item in Item.objects.select_related(
        'submitted_by', 'approved_by', 'returned_to', 'discarded_by'
    ).prefetch_related('claims'):
        items_data.append({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'category_display': item.get_category_display(),
            'description': item.description,
            'location_found': item.location_found,
            'date_found': str(item.date_found),
            'status': item.status,
            'status_display': item.get_status_display(),
            'submitted_by': item.submitted_by.username,
            'approved_by': item.approved_by.username if item.approved_by else None,
            'approval_date': item.approval_date.isoformat() if item.approval_date else None,
            'approval_notes': item.approval_notes,
            'returned_to': item.returned_to.username if item.returned_to else None,
            'discard_date': item.discard_date.isoformat() if item.discard_date else None,
            'discard_reason': item.discard_reason,
            'discard_notes': item.discard_notes,
            'created_at': item.created_at.isoformat(),
            'updated_at': item.updated_at.isoformat(),
        })

    claims_data = []
    for claim in Claim.objects.select_related('item', 'claimant', 'reviewed_by'):
        claims_data.append({
            'id': claim.id,
            'item_id': claim.item.id,
            'item_name': claim.item.name,
            'claimant': claim.claimant.username,
            'claim_type': claim.claim_type,
            'claim_type_display': claim.get_claim_type_display(),
            'description': claim.description,
            'contact_method': claim.contact_method,
            'additional_proof': claim.additional_proof,
            'status': claim.status,
            'status_display': claim.get_status_display(),
            'reviewed_by': claim.reviewed_by.username if claim.reviewed_by else None,
            'admin_notes': claim.admin_notes,
            'created_at': claim.created_at.isoformat(),
            'reviewed_at': claim.reviewed_at.isoformat() if claim.reviewed_at else None,
        })

    users_data = []
    for user in CustomUser.objects.prefetch_related('submitted_items', 'claims'):
        entry = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'user_type': user.user_type,
            'is_staff': user.is_staff,
            'approval_status': user.approval_status,
            'approval_date': user.approval_date.isoformat() if user.approval_date else None,
            'approved_by': user.approved_by.username if user.approved_by else None,
            'date_joined': user.date_joined.isoformat(),
            'items_submitted': list(user.submitted_items.values_list('id', flat=True)),
            'claims_made': list(user.claims.values_list('id', flat=True)),
        }
        if hasattr(user, 'student_profile'):
            entry['student_id'] = user.student_profile.student_id
            entry['grade'] = user.student_profile.grade
        if hasattr(user, 'teacher_profile'):
            entry['department'] = user.teacher_profile.department
        users_data.append(entry)

    data = {
        'recorded_at': timezone.now().isoformat(),
        'items': items_data,
        'claims': claims_data,
        'users': users_data,
        'instructions': [],
    }
    return JsonResponse(data)


@admin_only
@require_POST
def save_instructions(request):
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instructions.json')
    with open(path, 'w') as f:
        json.dump(body, f, indent=2)
    return JsonResponse({'status': 'saved'})


@admin_only
@require_POST
def begin_recording(request):
    now = time.time()
    expired = [t for t, v in list(_relogin_tokens.items()) if v['expires'] < now]
    for t in expired:
        del _relogin_tokens[t]
    token = secrets.token_urlsafe(32)
    _relogin_tokens[token] = {'user_id': request.user.id, 'expires': now + _TOKEN_EXPIRY}
    django_auth.logout(request)
    return JsonResponse({'token': token})


@require_POST
def relogin(request):
    try:
        body = json.loads(request.body)
        token = body.get('token', '')
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid'}, status=400)
    entry = _relogin_tokens.pop(token, None)
    if entry is None or time.time() > entry['expires']:
        return JsonResponse({'error': 'Invalid or expired token'}, status=403)
    try:
        user = CustomUser.objects.get(id=entry['user_id'])
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=403)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    django_auth.login(request, user)
    return JsonResponse({'status': 'ok'})


def simulate_home(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden()
    slider_items = Item.objects.filter(status__in=['unclaimed', 'rejected']).order_by('-created_at')[:8]
    return render(request, 'home.html', {
        'user': AnonymousUser(),
        'dev_simulate': True,
        'slider_items': slider_items,
    })


@admin_only
@require_GET
def get_instructions(request):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instructions.json')
    if not os.path.exists(path):
        return JsonResponse({'recorded_at': None, 'items': [], 'claims': [], 'users': [], 'instructions': []})
    with open(path) as f:
        data = json.load(f)
    return JsonResponse(data)


@admin_only
@require_POST
def load_snapshot(request):
    from django.utils.dateparse import parse_datetime
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Delete all items (claims cascade-delete via FK)
    Item.objects.all().delete()
    # Remove non-staff users (keep developer/admin accounts)
    CustomUser.objects.filter(is_staff=False).delete()

    # Restore users from snapshot
    user_map = {}
    for u in body.get('users', []):
        username = u.get('username', '')
        if not username:
            continue
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = CustomUser(username=username)
            user.set_password('demo1234')
        user.first_name = u.get('first_name', '')
        user.last_name = u.get('last_name', '')
        user.email = u.get('email', '')
        user.user_type = u.get('user_type', 'student')
        user.is_staff = bool(u.get('is_staff', False))
        user.approval_status = u.get('approval_status', 'pending')
        user.save()
        user_map[username] = user

    # Ensure the current (developer) user is always available
    user_map.setdefault(request.user.username, request.user)

    # Restore items, mapping old snapshot id -> new Item
    item_id_map = {}
    for item_data in body.get('items', []):
        submitted_by = user_map.get(item_data.get('submitted_by', ''))
        if not submitted_by:
            continue
        item = Item(
            name=item_data.get('name', ''),
            category=item_data.get('category', 'other'),
            description=item_data.get('description', ''),
            location_found=item_data.get('location_found', ''),
            date_found=item_data.get('date_found') or str(timezone.now().date()),
            status=item_data.get('status', 'reported'),
            submitted_by=submitted_by,
            approval_notes=item_data.get('approval_notes', ''),
            discard_reason=item_data.get('discard_reason', ''),
            discard_notes=item_data.get('discard_notes', ''),
        )
        if item_data.get('approved_by'):
            item.approved_by = user_map.get(item_data['approved_by'])
        if item_data.get('returned_to'):
            item.returned_to = user_map.get(item_data['returned_to'])
        if item_data.get('approval_date'):
            item.approval_date = parse_datetime(item_data['approval_date'])
        if item_data.get('discard_date'):
            item.discard_date = parse_datetime(item_data['discard_date'])
        if item_data.get('verified_date'):
            item.verified_date = parse_datetime(item_data['verified_date'])
        item.save()
        item_id_map[item_data.get('id')] = item

    # Restore claims
    for claim_data in body.get('claims', []):
        item = item_id_map.get(claim_data.get('item_id'))
        claimant = user_map.get(claim_data.get('claimant', ''))
        if not item or not claimant:
            continue
        claim = Claim(
            item=item,
            claimant=claimant,
            claim_type=claim_data.get('claim_type', 'claim'),
            description=claim_data.get('description', ''),
            contact_method=claim_data.get('contact_method', ''),
            additional_proof=claim_data.get('additional_proof', ''),
            status=claim_data.get('status', 'pending'),
            admin_notes=claim_data.get('admin_notes', ''),
        )
        if claim_data.get('reviewed_by'):
            claim.reviewed_by = user_map.get(claim_data['reviewed_by'])
        if claim_data.get('reviewed_at'):
            claim.reviewed_at = parse_datetime(claim_data['reviewed_at'])
        claim.save()

    return JsonResponse({'status': 'ok'})
