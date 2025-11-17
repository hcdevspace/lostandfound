# SQL, PostgreSQL, Keys & Django ORM - Concise Guide

## SQL Basics

**SQL (Structured Query Language)** - Language for managing relational databases

**Core Operations (CRUD):**
```sql
-- Create
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');

-- Read
SELECT * FROM users WHERE id = 1;

-- Update
UPDATE users SET email = 'newemail@example.com' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
```

---

## PostgreSQL

**PostgreSQL** - Advanced, open-source relational database

**Key Features:**
- ACID compliant (Atomicity, Consistency, Isolation, Durability)
- Advanced data types (JSON, Arrays, UUID, Geometry)
- Full-text search
- JSONB for efficient JSON storage
- Powerful indexing (B-tree, Hash, GiST, GIN)
- Supports complex queries and transactions

---

## Primary Keys

**Definition:** Unique identifier for each row in a table

**Characteristics:**
- Must be UNIQUE
- Cannot be NULL
- Only ONE primary key per table
- Auto-incrementing (usually)

### Primary Key Examples

**PostgreSQL:**
```sql
-- Method 1: Inline definition
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(255)
);

-- Method 2: Separate constraint
CREATE TABLE products (
    product_id INT,
    name VARCHAR(200),
    price DECIMAL(10,2),
    PRIMARY KEY (product_id)
);

-- Method 3: Composite primary key
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrolled_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

**Data Types for Primary Keys:**
```sql
SERIAL          -- Auto-incrementing integer (1, 2, 3...)
BIGSERIAL       -- Large auto-incrementing integer
UUID            -- Universally unique identifier
INTEGER         -- Manual integer
```

### Primary Key in Action

```sql
-- Create table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE
);

-- Insert (ID auto-generated)
INSERT INTO customers (name, email) 
VALUES ('Alice', 'alice@example.com');

-- Result: customer_id = 1 (automatically assigned)

-- Query by primary key (very fast)
SELECT * FROM customers WHERE customer_id = 1;
```

---

## Foreign Keys

**Definition:** Links one table to another, establishing relationships

**Characteristics:**
- References PRIMARY KEY in another table
- Enforces referential integrity
- Multiple foreign keys allowed per table
- Can be NULL (optional relationship)

### Foreign Key Examples

**One-to-Many Relationship:**
```sql
-- Parent table (one)
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- Child table (many)
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
```

**Visual Representation:**
```
┌─────────────────┐           ┌─────────────────┐
│    authors      │           │     books       │
├─────────────────┤           ├─────────────────┤
│ author_id (PK)  │◄──────────│ book_id (PK)    │
│ name            │    1:N    │ title           │
└─────────────────┘           │ author_id (FK)  │
                              └─────────────────┘
```

### Foreign Key Actions

**ON DELETE Options:**
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE      -- Delete orders when customer deleted
);

-- Other options:
ON DELETE SET NULL            -- Set FK to NULL
ON DELETE SET DEFAULT         -- Set FK to default value
ON DELETE RESTRICT            -- Prevent deletion (error)
ON DELETE NO ACTION           -- Similar to RESTRICT
```

**ON UPDATE Options:**
```sql
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    ON UPDATE CASCADE         -- Update FK when PK changes
```

### Complete Foreign Key Example

```sql
-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Posts table (references users)
CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(user_id) 
        ON DELETE CASCADE
);

-- Comments table (references both posts and users)
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

**Relationship Diagram:**
```
users (1) ──→ posts (N)
  ↓
  └──────────→ comments (N)
                   ↑
posts (1) ─────────┘
```

### Querying with Foreign Keys

```sql
-- Join tables using foreign keys
SELECT 
    posts.title,
    users.username AS author,
    posts.created_at
FROM posts
JOIN users ON posts.author_id = users.user_id
WHERE users.username = 'john';

-- Get post with all comments
SELECT 
    p.title,
    u.username AS author,
    c.comment_text,
    cu.username AS commenter
FROM posts p
JOIN users u ON p.author_id = u.user_id
LEFT JOIN comments c ON c.post_id = p.post_id
LEFT JOIN users cu ON c.user_id = cu.user_id
WHERE p.post_id = 1;
```

---

## Django ORM (Object-Relational Mapping)

**What is ORM?**
ORM translates between Python objects and database tables, eliminating the need to write SQL.

**Benefits:**
- Write Python instead of SQL
- Database-agnostic (switch databases easily)
- Protection against SQL injection
- Cleaner, more maintainable code
- Built-in migrations

### Django Models = Database Tables

**SQL vs Django ORM:**

**SQL (PostgreSQL):**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Django ORM (models.py):**
```python
from django.db import models

class User(models.Model):
    # id is created automatically as primary key
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

Django automatically:
- Creates `id` field as PRIMARY KEY
- Generates SQL CREATE TABLE
- Handles database schema

---

## Primary Keys in Django

**Automatic Primary Key:**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Django auto-creates: id = models.AutoField(primary_key=True)
```

**Custom Primary Key:**
```python
class Product(models.Model):
    product_code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

**UUID Primary Key:**
```python
import uuid

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_date = models.DateTimeField(auto_now_add=True)
```

---

## Foreign Keys in Django

### One-to-Many Relationship

**Django Model:**
```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='books'
    )
    published_date = models.DateField()
```

**Generated SQL:**
```sql
CREATE TABLE app_author (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(254)
);

CREATE TABLE app_book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author_id INTEGER REFERENCES app_author(id) ON DELETE CASCADE,
    published_date DATE
);
```

**Querying:**
```python
# Forward relationship (book → author)
book = Book.objects.get(id=1)
author_name = book.author.name

# Reverse relationship (author → books)
author = Author.objects.get(id=1)
books = author.books.all()  # 'books' from related_name
```

### on_delete Options in Django

```python
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # CASCADE: Delete posts when user deleted

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # SET_NULL: Set author to NULL when user deleted

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    # PROTECT: Prevent user deletion if posts exist

    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    # SET_DEFAULT: Set to default value when user deleted

    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # DO_NOTHING: No action (can cause integrity errors)
```

### Many-to-Many Relationship

**Django Model:**
```python
class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    title = models.CharField(max_length=200)
    students = models.ManyToManyField(Student, related_name='courses')
```

**Generated SQL (creates junction table):**
```sql
CREATE TABLE app_student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE app_course (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200)
);

CREATE TABLE app_course_students (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES app_course(id),
    student_id INTEGER REFERENCES app_student(id)
);
```

**Querying:**
```python
# Add students to course
course = Course.objects.get(id=1)
student = Student.objects.get(id=1)
course.students.add(student)

# Get all courses for a student
student.courses.all()

# Get all students in a course
course.students.all()
```

### One-to-One Relationship

```python
class User(models.Model):
    username = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField()
    avatar = models.ImageField()
```

**Querying:**
```python
# Access profile from user
user = User.objects.get(id=1)
bio = user.profile.bio

# Access user from profile
profile = Profile.objects.get(id=1)
username = profile.user.username
```

---

## Complete Example: Blog System

### SQL (PostgreSQL)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(255) UNIQUE
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    author_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query
SELECT p.title, u.username, c.text
FROM posts p
JOIN users u ON p.author_id = u.id
LEFT JOIN comments c ON c.post_id = p.id
WHERE p.id = 1;
```

### Django ORM

```python
# models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Query
post = Post.objects.select_related('author').prefetch_related('comments__user').get(id=1)
print(post.title)
print(post.author.username)
for comment in post.comments.all():
    print(f"{comment.user.username}: {comment.text}")
```

---

## ORM Query Examples

**SQL → Django ORM Translation:**

```python
# CREATE
user = User.objects.create(username='john', email='john@example.com')

# READ
users = User.objects.all()                    # SELECT * FROM users
user = User.objects.get(id=1)                # WHERE id = 1
users = User.objects.filter(username='john') # WHERE username = 'john'

# UPDATE
user.email = 'new@example.com'
user.save()

# DELETE
user.delete()

# JOIN
posts = Post.objects.select_related('author')  # JOIN with author
# Equivalent SQL: SELECT * FROM posts JOIN users ON posts.author_id = users.id

# WHERE with foreign key
johns_posts = Post.objects.filter(author__username='john')
# SQL: SELECT * FROM posts JOIN users WHERE users.username = 'john'

# Count
post_count = Post.objects.count()

# Ordering
recent_posts = Post.objects.order_by('-created_at')

# Limit
top_5 = Post.objects.all()[:5]
```

---

## Key Concepts Summary

### Primary Key
- **SQL:** `id SERIAL PRIMARY KEY`
- **Django:** Automatically created as `id` field
- **Purpose:** Unique identifier for each record

### Foreign Key
- **SQL:** `FOREIGN KEY (user_id) REFERENCES users(id)`
- **Django:** `models.ForeignKey(User, on_delete=models.CASCADE)`
- **Purpose:** Link tables, maintain referential integrity

### Django ORM Benefits
- Write Python, not SQL
- Automatic migrations
- Query optimization
- Database portability
- Security (SQL injection prevention)

### Relationship Types
- **One-to-Many:** ForeignKey
- **Many-to-Many:** ManyToManyField
- **One-to-One:** OneToOneField
