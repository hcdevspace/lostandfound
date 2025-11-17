# HTTP Protocol - Concise Overview

## What is HTTP?

**HTTP (HyperText Transfer Protocol)** is the foundation of data communication on the web. It's a stateless, request-response protocol between clients and servers.

- **Stateless:** Each request is independent
- **Text-based:** Human-readable (HTTP/1.x)
- **Port:** 80 (HTTP), 443 (HTTPS)
- **Application Layer:** Runs on top of TCP/IP

## HTTP Request-Response Cycle

```
┌────────┐                           ┌────────┐
│ Client │ ─── HTTP Request ──────→  │ Server │
│        │                           │        │
│        │ ←── HTTP Response ─────   │        │
└────────┘                           └────────┘
```

## Request Structure

```http
GET /api/users/123 HTTP/1.1          ← Request Line (Method, Path, Version)
Host: api.example.com                 ← Headers (metadata)
Authorization: Bearer token123
Content-Type: application/json
                                      ← Blank line
{"key": "value"}                      ← Body (optional)
```

## HTTP Methods

| Method | Purpose | Example Use |
|--------|---------|-------------|
| **GET** | Retrieve data | Get user profile |
| **POST** | Create resource | Register new user |
| **PUT** | Replace resource | Update entire user record |
| **PATCH** | Modify resource | Update user email only |
| **DELETE** | Remove resource | Delete user account |
| **HEAD** | Get headers only | Check if resource exists |
| **OPTIONS** | Check allowed methods | CORS preflight |

## Response Structure

```http
HTTP/1.1 200 OK                       ← Status Line (Version, Code, Message)
Content-Type: application/json        ← Headers
Content-Length: 87
Cache-Control: max-age=3600
                                      ← Blank line
{"id": 123, "name": "John"}           ← Body
```

## Status Code Categories

### 1xx - Informational
- **100 Continue** - Continue with request

### 2xx - Success
- **200 OK** - Request succeeded
- **201 Created** - Resource created
- **204 No Content** - Success, no body

### 3xx - Redirection
- **301 Moved Permanently** - Resource moved
- **302 Found** - Temporary redirect
- **304 Not Modified** - Use cached version

### 4xx - Client Errors
- **400 Bad Request** - Invalid syntax
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Access denied
- **404 Not Found** - Resource doesn't exist
- **429 Too Many Requests** - Rate limited

### 5xx - Server Errors
- **500 Internal Server Error** - Server error
- **502 Bad Gateway** - Invalid upstream response
- **503 Service Unavailable** - Server down

## Essential Headers

### Request Headers
```http
Host: www.example.com               # Required in HTTP/1.1
User-Agent: Mozilla/5.0             # Client info
Accept: application/json            # Accepted response types
Authorization: Bearer <token>       # Authentication
Content-Type: application/json      # Request body format
Cookie: session=abc123              # Session data
```

### Response Headers
```http
Content-Type: application/json      # Response body format
Content-Length: 1234                # Body size
Cache-Control: max-age=3600         # Caching rules
Set-Cookie: session=xyz; HttpOnly   # Set client cookie
Location: /new-url                  # Redirect URL
ETag: "abc123"                      # Resource version
```

## HTTP Versions

| Version | Key Feature |
|---------|-------------|
| **HTTP/1.0** | Basic protocol, new connection per request |
| **HTTP/1.1** | Persistent connections, chunked transfer |
| **HTTP/2** | Binary protocol, multiplexing, header compression |
| **HTTP/3** | QUIC (UDP-based), faster, more reliable |

## HTTPS (HTTP Secure)

```
HTTP + TLS/SSL = HTTPS
```

- **Encryption:** Data encrypted in transit
- **Authentication:** Verify server identity via certificates
- **Integrity:** Detect tampering
- **Port:** 443 (default)

## Common Content Types

```http
Content-Type: text/html                    # HTML pages
Content-Type: application/json             # JSON data
Content-Type: application/xml              # XML data
Content-Type: multipart/form-data          # File uploads
Content-Type: application/x-www-form-urlencoded  # Form submissions
Content-Type: text/plain                   # Plain text
Content-Type: image/jpeg                   # JPEG images
```

## Caching Directives

```http
Cache-Control: no-cache                    # Always validate with server
Cache-Control: no-store                    # Don't cache at all
Cache-Control: max-age=3600                # Cache for 1 hour
Cache-Control: public                      # Can be cached by anyone
Cache-Control: private                     # Only client can cache
```

## Request Example Flow

```
1. Client Request:
   GET /api/products/42 HTTP/1.1
   Host: api.shop.com
   Accept: application/json

2. Server Processing:
   - Parse request
   - Route to handler
   - Query database
   - Build response

3. Server Response:
   HTTP/1.1 200 OK
   Content-Type: application/json
   
   {"id": 42, "name": "Laptop", "price": 999}
```

## Key Concepts

### Stateless
- Server doesn't remember previous requests
- Use cookies/tokens for session management

### Idempotency
- **Idempotent:** Multiple identical requests = same result (GET, PUT, DELETE)
- **Not Idempotent:** Multiple requests = different results (POST)

### Safe Methods
- **Safe:** Don't modify server state (GET, HEAD, OPTIONS)
- **Unsafe:** Modify server state (POST, PUT, DELETE, PATCH)

### Connection Management

**HTTP/1.0 - New connection per request**
```
Request 1 → Connection → Response → Close
Request 2 → Connection → Response → Close
```

**HTTP/1.1 - Persistent connection**
```
Connection → Request 1 → Response
          → Request 2 → Response
          → Request 3 → Response → Close
```

## Authentication Methods

```http
# Basic Auth (Base64 encoded)
Authorization: Basic dXNlcjpwYXNzd29yZA==

# Bearer Token (JWT, OAuth)
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# API Key
X-API-Key: abc123xyz789
```

## CORS (Cross-Origin Resource Sharing)

Allows browsers to make requests across different domains.

```http
# Preflight Request (OPTIONS)
Origin: https://example.com
Access-Control-Request-Method: POST

# Response
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: Content-Type
```

## URL Structure

```
https://api.example.com:443/users/123?active=true#profile
│     │ │              │   │         │          │
│     │ │              │   │         │          └─ Fragment
│     │ │              │   │         └─ Query parameters
│     │ │              │   └─ Path
│     │ │              └─ Port
│     │ └─ Domain
│     └─ Scheme (protocol)
```

## Summary

HTTP is a simple, stateless protocol that powers the web:
- **Client sends request** → Server processes → **Server sends response**
- **Methods** define action (GET, POST, PUT, DELETE, etc.)
- **Status codes** indicate outcome (200 OK, 404 Not Found, 500 Error, etc.)
- **Headers** provide metadata
- **Body** contains actual data
- **HTTPS** adds encryption for security
