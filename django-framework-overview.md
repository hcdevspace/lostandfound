# Django Framework - Concise Guide

## What is Django?

**Django** is a high-level Python web framework that enables rapid development of secure, scalable web applications.

**Key Features:**
- **Batteries included:** Built-in admin, authentication, ORM, forms, etc.
- **Secure:** Protection against SQL injection, XSS, CSRF, clickjacking
- **Scalable:** Used by Instagram, Pinterest, Spotify, YouTube
- **Fast development:** Less code, more functionality
- **Python-powered:** Clean, readable syntax

**Philosophy:** "Don't Repeat Yourself" (DRY)

## MVT Architecture

Django follows the **MVT (Model-View-Template)** pattern, a variation of MVC (Model-View-Controller).

```
┌─────────────────────────────────────────────────────────┐
│                     Django MVT Flow                      │
└─────────────────────────────────────────────────────────┘

     Browser Request
           ↓
    ┌──────────┐
    │   URLs   │  → Maps URL to View
    └─────┬────┘
          ↓
    ┌──────────┐
    │   VIEW   │  → Business Logic (Controller)
    └─────┬────┘
          ↓
    ┌──────────┐         ┌──────────┐
    │  MODEL   │ ←────→  │ Database │
    └─────┬────┘         └──────────┘
          ↓
    ┌──────────┐
    │ TEMPLATE │  → Presentation Layer
    └─────┬────┘
          ↓
     HTML Response
```

### MVT vs MVC Comparison

| Component | Django (MVT) | Traditional (MVC) |
|-----------|--------------|-------------------|
| **Model** | Model | Model |
| **View** | Template | View |
| **Controller** | View | Controller |

Django's "View" acts as the controller, and "Template" handles presentation.

---

## 1. MODEL - Data Layer

**Purpose:** Defines data structure and database schema

**What it does:**
- Define database tables as Python classes
- Handle database operations (CRUD)
- Data validation and relationships
- Business logic related to data

### Model Example

```python
# models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

### Model Features

**Field Types:**
```python
CharField(max_length=100)          # Short text
TextField()                        # Long text
IntegerField()                     # Integer
DecimalField(max_digits=10, decimal_places=2)  # Decimal
BooleanField(default=False)        # True/False
DateField()                        # Date
DateTimeField(auto_now_add=True)   # Timestamp
EmailField()                       # Email validation
URLField()                         # URL validation
FileField(upload_to='uploads/')    # File upload
ImageField(upload_to='images/')    # Image upload
JSONField()                        # JSON data
```

**Relationships:**
```python
# One-to-Many
author = models.ForeignKey(User, on_delete=models.CASCADE)

# Many-to-Many
tags = models.ManyToManyField(Tag)

# One-to-One
profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
```

**ORM Queries:**
```python
# Create
user = User.objects.create(username='john', email='john@example.com')

# Read
all_users = User.objects.all()
user = User.objects.get(id=1)
active_users = User.objects.filter(is_active=True)

# Update
user.email = 'newemail@example.com'
user.save()

# Delete
user.delete()

# Complex queries
posts = Post.objects.filter(
    author__username='john',
    published_date__year=2025
).order_by('-published_date')
```

---

## 2. VIEW - Controller/Logic Layer

**Purpose:** Handles business logic and request processing

**What it does:**
- Receive HTTP requests
- Process data (fetch from models)
- Apply business logic
- Return HTTP responses

### View Types

**Function-Based Views (FBV)**
```python
# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Post

def post_list(request):
    """Display all posts"""
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})

def post_detail(request, post_id):
    """Display single post"""
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/detail.html', {'post': post})

def post_create(request):
    """Create new post"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return JsonResponse({'success': True, 'id': post.id})
    return render(request, 'posts/create.html')
```

**Class-Based Views (CBV)**
```python
from django.views.generic import ListView, DetailView, CreateView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/create.html'
    success_url = '/posts/'
```

**API Views (Django REST Framework)**
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def post_api(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return Response({'posts': list(posts.values())})
    
    elif request.method == 'POST':
        post = Post.objects.create(**request.data)
        return Response({'id': post.id}, status=201)
```

### URL Routing

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    
    # Class-based views
    path('posts/', views.PostListView.as_view(), name='posts'),
]
```

---

## 3. TEMPLATE - Presentation Layer

**Purpose:** Renders HTML with dynamic data

**What it does:**
- Display data from views
- Generate dynamic HTML
- Handle user interface logic
- Template inheritance and reusability

### Template Syntax

**Variables:**
```django
{{ variable }}
{{ user.username }}
{{ post.title|upper }}
```

**Tags:**
```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please log in</p>
{% endif %}

{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% empty %}
    <p>No posts found</p>
{% endfor %}
```

**Filters:**
```django
{{ text|truncatewords:30 }}        # Limit words
{{ date|date:"Y-m-d" }}            # Format date
{{ price|floatformat:2 }}          # 2 decimal places
{{ name|lower }}                   # Lowercase
{{ content|safe }}                 # Don't escape HTML
{{ items|length }}                 # Count items
```

### Template Example

**Base Template (base.html):**
```django
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav>
        <a href="{% url 'home' %}">Home</a>
        <a href="{% url 'post_list' %}">Posts</a>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2025 My Site</p>
    </footer>
</body>
</html>
```

**Child Template (post_list.html):**
```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Posts - {{ block.super }}{% endblock %}

{% block content %}
    <h1>All Posts</h1>
    
    {% if posts %}
        {% for post in posts %}
            <article>
                <h2>
                    <a href="{% url 'post_detail' post.id %}">
                        {{ post.title }}
                    </a>
                </h2>
                <p>By {{ post.author.username }}</p>
                <p>{{ post.content|truncatewords:50 }}</p>
                <small>{{ post.published_date|date:"F d, Y" }}</small>
            </article>
        {% endfor %}
    {% else %}
        <p>No posts available</p>
    {% endif %}
{% endblock %}
```

---

## Complete MVT Flow Example

### 1. Define Model
```python
# models.py
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
```

### 2. Create View
```python
# views.py
def product_list(request):
    products = Product.objects.filter(stock__gt=0)
    return render(request, 'products/list.html', {
        'products': products
    })
```

### 3. Configure URL
```python
# urls.py
urlpatterns = [
    path('products/', views.product_list, name='products'),
]
```

### 4. Create Template
```django
<!-- templates/products/list.html -->
{% for product in products %}
    <div>
        <h3>{{ product.name }}</h3>
        <p>Price: ${{ product.price }}</p>
        <p>Stock: {{ product.stock }}</p>
    </div>
{% endfor %}
```

---

## Django Project Structure

```
myproject/
│
├── manage.py                  # Command-line utility
├── myproject/                 # Project settings
│   ├── __init__.py
│   ├── settings.py           # Configuration
│   ├── urls.py               # Root URL routing
│   └── wsgi.py               # WSGI application
│
└── myapp/                     # Application
    ├── migrations/           # Database migrations
    ├── __init__.py
    ├── admin.py              # Admin interface
    ├── apps.py               # App configuration
    ├── models.py             # Models (M)
    ├── views.py              # Views (V)
    ├── urls.py               # App URLs
    ├── templates/            # Templates (T)
    │   └── myapp/
    │       └── page.html
    └── static/               # Static files (CSS/JS)
        └── myapp/
            └── style.css
```

## Key Django Features

**Admin Interface:**
```python
# admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    search_fields = ['title', 'content']
    list_filter = ['published_date']
```

**Forms:**
```python
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```

**Authentication:**
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
```

## Summary

**Django MVT Pattern:**
- **Model:** Data structure and database (ORM)
- **View:** Business logic and request handling (Controller)
- **Template:** HTML presentation (UI)

**Flow:** Request → URL → View → Model → Template → Response

**Benefits:**
- Clear separation of concerns
- Reusable components
- Easy maintenance
- Rapid development
