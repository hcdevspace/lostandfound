# Django + PostgreSQL Client-Server Architecture

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                        CLIENT                           │
│  (Web Browser, Mobile App, API Client, Desktop App)    │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS Requests
                     │ (GET, POST, PUT, DELETE)
                     ↓
┌─────────────────────────────────────────────────────────┐
│                   DJANGO APPLICATION                    │
│                    (Application Server)                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │  WSGI/ASGI Server (Gunicorn/Uvicorn)             │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│  ┌────────────────▼─────────────────────────────────┐  │
│  │  Django Framework                                │  │
│  │  • URL Router                                    │  │
│  │  • Views (Business Logic)                        │  │
│  │  • Middleware                                    │  │
│  │  • ORM (Object-Relational Mapping)              │  │
│  │  • Templates/Serializers                        │  │
│  │  • Static File Handler (WhiteNoise)             │  │
│  └────────────────┬─────────────────────────────────┘  │
└───────────────────┼─────────────────────────────────────┘
                    │
                    │ SQL Queries via psycopg2
                    │ (SELECT, INSERT, UPDATE, DELETE)
                    ↓
┌─────────────────────────────────────────────────────────┐
│                  POSTGRESQL DATABASE                    │
│  • Tables & Indexes                                     │
│  • Constraints & Triggers                               │
│  • Stored Procedures                                    │
│  • Transaction Management                               │
└─────────────────────────────────────────────────────────┘
```

## Request-Response Flow

### 1. Client Request
```
Client → HTTP Request → Django Server (Port 8000)
Example: GET /api/users/123/
```

### 2. Django Processing
```
Request
  ↓
Middleware (Security, Session, CSRF, Auth)
  ↓
URL Router (urls.py) → Matches URL pattern
  ↓
View Function/Class (views.py) → Business logic
  ↓
Model/ORM (models.py) → Generates SQL query
  ↓
PostgreSQL Adapter (psycopg2)
```

### 3. Database Interaction
```
Django ORM
  ↓
SQL Query → SELECT * FROM users WHERE id=123
  ↓
PostgreSQL executes query
  ↓
Returns result set
  ↓
Django ORM converts to Python objects
```

### 4. Response Generation
```
View processes data
  ↓
Serializes data (JSON/HTML)
  ↓
Template rendering (if HTML)
  ↓
Middleware processes response
  ↓
HTTP Response → Client
```

## Key Components

### Client Layer
**Purpose:** User interface and interaction

**Types:**
- **Web Browser:** Renders HTML/CSS/JavaScript
- **Mobile App:** Native iOS/Android or React Native
- **API Client:** Third-party services, microservices
- **CLI Tools:** Command-line applications

**Communication:** HTTP/HTTPS requests (REST API or HTML pages)

---

### Django Application Server
**Purpose:** Business logic, request handling, data processing

**Core Components:**

1. **WSGI/ASGI Server**
   - Gunicorn (WSGI) - synchronous requests
   - Uvicorn (ASGI) - async/WebSocket support
   - Handles concurrent requests

2. **URL Dispatcher**
   - Maps URLs to views
   - Pattern matching with regex or path converters
   - Namespace organization

3. **Views**
   - Function-based views (FBV)
   - Class-based views (CBV)
   - REST API views (Django REST Framework)

4. **Middleware**
   - Request/response processing pipeline
   - Authentication, security, sessions
   - Custom logic injection

5. **Django ORM**
   - Database abstraction layer
   - Translates Python code to SQL
   - Model definitions = Database schema
   - Query optimization and caching

6. **Static File Handling**
   - WhiteNoise middleware serves static files
   - CSS, JavaScript, images
   - No separate web server needed

---

### PostgreSQL Database Server
**Purpose:** Persistent data storage and retrieval

**Key Features:**
- **ACID Compliance:** Reliable transactions
- **Data Integrity:** Foreign keys, constraints, triggers
- **Advanced Types:** JSON, Arrays, UUID, Geometric
- **Indexing:** B-tree, Hash, GiST, GIN for performance
- **Full-Text Search:** Built-in search capabilities
- **Connection Pooling:** Efficient connection reuse

**Django-PostgreSQL Connection:**
- Uses `psycopg2` or `psycopg2-binary` adapter
- Connection pooling via `CONN_MAX_AGE` setting
- Persistent connections reduce overhead

## Data Flow Example

### Example: Fetching User Profile

```python
# 1. Client Request
GET /users/123/profile/

# 2. Django URL Router (urls.py)
path('users/<int:user_id>/profile/', views.user_profile)

# 3. View (views.py)
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)  # ORM query
    return JsonResponse({'name': user.name, 'email': user.email})

# 4. Django ORM generates SQL
SELECT id, name, email FROM auth_user WHERE id = 123;

# 5. PostgreSQL executes and returns data
{'id': 123, 'name': 'John Doe', 'email': 'john@example.com'}

# 6. Django serializes and sends response
HTTP 200 OK
Content-Type: application/json
{"name": "John Doe", "email": "john@example.com"}
```

## Deployment Configurations

### Development
```bash
# Single process, auto-reload, debug toolbar
python manage.py runserver 0.0.0.0:8000
```

### Production
```bash
# Multiple worker processes
gunicorn myproject.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --threads 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
```

### Key Settings
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}

ALLOWED_HOSTS = ['yourdomain.com', 'your-server-ip']
DEBUG = False  # Never True in production
```

## Architecture Benefits

✅ **Separation of Concerns:** Client, application, and data layers are independent  
✅ **Scalability:** Can scale Django servers horizontally (multiple instances)  
✅ **Security:** Django handles authentication, CSRF, SQL injection prevention  
✅ **Database Abstraction:** ORM makes switching databases easier  
✅ **Maintainability:** Clear separation makes debugging and updates simpler  
✅ **Performance:** Connection pooling, query optimization, caching layers  

## Common Communication Patterns

### REST API (JSON)
```
Client ←→ JSON ←→ Django REST Framework ←→ PostgreSQL
```

### Traditional Web App (HTML)
```
Browser ←→ HTML/CSS/JS ←→ Django Templates ←→ PostgreSQL
```

### Real-time (WebSockets)
```
Client ←→ WebSocket ←→ Django Channels (ASGI) ←→ PostgreSQL
```
