# Databases, SQL & Relationships - Concise Guide

## Why Use Databases?

**Problem:** Applications need to store data permanently and efficiently.

**Without Database:**
```python
# Bad: Storing in files
users = []  # Lost when program stops
# or
with open('users.txt', 'w') as f:
    f.write(user_data)  # Hard to query, no relationships, no concurrent access
```

**With Database:**
- **Persistent Storage:** Data survives after program ends
- **Concurrent Access:** Multiple users can access simultaneously
- **Data Integrity:** Enforces rules (unique emails, valid data)
- **Efficient Queries:** Fast search across millions of records
- **Relationships:** Connect related data (users → posts → comments)
- **Security:** Access control, encryption
- **Backup & Recovery:** Protect against data loss
- **ACID Transactions:** All-or-nothing operations (bank transfers)

---

## Purpose of SQL

**SQL (Structured Query Language)** - Language to interact with databases

**Core Operations:**
```sql
CREATE TABLE users (id INT, name VARCHAR(100));     -- Structure data
INSERT INTO users VALUES (1, 'John');                -- Add data
SELECT * FROM users WHERE id = 1;                    -- Read data
UPDATE users SET name = 'Jane' WHERE id = 1;         -- Modify data
DELETE FROM users WHERE id = 1;                      -- Remove data
```

**Why SQL?**
- Standard language across all databases (MySQL, PostgreSQL, Oracle)
- Declarative (say *what* you want, not *how* to get it)
- Powerful querying (filtering, sorting, joining)
- Data definition (create tables, relationships)

---

## Database Relationships

### Primary Key (PK)

**Purpose:** Uniquely identify each row

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,    -- Auto-incrementing unique ID
    username VARCHAR(100),
    email VARCHAR(255)
);
```

**Rules:**
- Must be UNIQUE
- Cannot be NULL
- One per table
- Fast lookups

**Why?**
- Reference rows from other tables
- Ensure each record is distinct
- Optimize queries

---

### Foreign Key (FK)

**Purpose:** Link tables together, establish relationships

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES users(id)
);
```

**Rules:**
- Must reference a PRIMARY KEY in another table
- Enforces referential integrity (can't create post with invalid author)
- Can have multiple per table

**Why?**
- Connect related data
- Maintain data consistency
- Enable complex queries across tables

---

## Relationship Types

### 1. One-to-Many (1:N)

**Most Common Relationship**

**Example:** One author → Many books

```
┌──────────┐         ┌──────────┐
│ authors  │         │  books   │
├──────────┤         ├──────────┤
│ id (PK)  │◄───────┤ id (PK)  │
│ name     │    1:N  │ title    │
└──────────┘         │author_id │
                     │   (FK)   │
                     └──────────┘
```

**SQL:**
```sql
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);
```

**Django ORM:**
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

**Real-World Examples:**
- User → Posts
- Customer → Orders
- Department → Employees
- Category → Products

---

### 2. Many-to-Many (N:M)

**Example:** Students ↔ Courses (students take multiple courses, courses have multiple students)

```
┌──────────┐    ┌────────────────┐    ┌──────────┐
│ students │    │  enrollments   │    │ courses  │
├──────────┤    ├────────────────┤    ├──────────┤
│ id (PK)  │◄──┤ student_id (FK)│    │ id (PK)  │
│ name     │    │ course_id (FK) │──►│ title    │
└──────────┘    └────────────────┘    └──────────┘
                  (Junction Table)
```

**SQL:**
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200)
);

CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

**Django ORM:**
```python
class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    title = models.CharField(max_length=200)
    students = models.ManyToManyField(Student)
```

Django automatically creates the junction table.

**Real-World Examples:**
- Users ↔ Roles
- Products ↔ Categories
- Authors ↔ Books (when books have multiple authors)
- Tags ↔ Posts

---

### 3. One-to-One (1:1)

**Example:** One user → One profile

```
┌──────────┐         ┌──────────┐
│  users   │         │ profiles │
├──────────┤         ├──────────┤
│ id (PK)  │◄───────┤ id (PK)  │
│ username │    1:1  │ user_id  │
└──────────┘         │   (FK)   │
                     │ bio      │
                     │ avatar   │
                     └──────────┘
```

**SQL:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100)
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    bio TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Django ORM:**
```python
class User(models.Model):
    username = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
```

**Real-World Examples:**
- User ↔ Profile
- Employee ↔ Parking Spot
- Country ↔ Capital City
- Person ↔ Passport

---

## Django ORM Overview

**What is ORM?**
Object-Relational Mapping - Write Python instead of SQL

**Without ORM (Raw SQL):**
```python
cursor.execute("SELECT * FROM users WHERE username = %s", ['john'])
result = cursor.fetchone()
```

**With Django ORM:**
```python
user = User.objects.get(username='john')
```

### Key Benefits

1. **No SQL Required**
```python
# Django ORM
users = User.objects.filter(age__gte=18)

# Generates SQL:
# SELECT * FROM users WHERE age >= 18
```

2. **Database Agnostic**
```python
# Same code works with PostgreSQL, MySQL, SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Just change this
        'NAME': 'mydb',
    }
}
```

3. **Automatic Foreign Keys**
```python
# Access related objects
book = Book.objects.get(id=1)
author_name = book.author.name  # Automatic join

# Reverse access
author = Author.objects.get(id=1)
books = author.book_set.all()  # Get all books by this author
```

4. **Protection**
```python
# SQL Injection prevented automatically
User.objects.filter(username=user_input)  # Safe
```

### Foreign Key Behavior

**on_delete Options:**
```python
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # CASCADE: Delete posts when user deleted
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # SET_NULL: Keep post, remove author reference
    
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    # PROTECT: Prevent user deletion if posts exist
```

---

## Complete Example: Blog System

**Relationships:**
- User → Posts (1:N)
- Post → Comments (1:N)
- User → Comments (1:N)

**Django Models:**
```python
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Generated Database Structure:**
```
users (PK: id)
  └─ posts (PK: id, FK: author_id → users.id)
       └─ comments (PK: id, FK: post_id → posts.id)
  └─ comments (FK: user_id → users.id)
```

**Usage:**
```python
# Create
user = User.objects.create(username='john', email='john@example.com')
post = Post.objects.create(title='Hello', content='World', author=user)
comment = Comment.objects.create(post=post, user=user, text='Nice post!')

# Query with relationships
post = Post.objects.get(id=1)
print(post.author.username)  # Access author
print(post.comment_set.count())  # Count comments

# All posts by a user
johns_posts = Post.objects.filter(author__username='john')
```

---

## Summary

### Why Database?
- Persistent, efficient storage
- Handle concurrent users
- Maintain data integrity
- Query millions of records fast

### SQL Purpose
- Standard language for databases
- Define structure, query data
- Manage relationships

### Keys
- **Primary Key:** Unique identifier (id)
- **Foreign Key:** Links tables together

### Relationships
- **One-to-Many:** User → Posts (most common)
- **Many-to-Many:** Students ↔ Courses (junction table)
- **One-to-One:** User ↔ Profile (split data)

### Django ORM
- Write Python, not SQL
- Automatic relationships
- Database-agnostic
- Built-in security
