# Lost and Found - School Management System

## Project Description
A Django web application to help students and staff report found items, search for lost belongings, and manage the claim process efficiently.

## Team Members
- Harshit, Aaryan, Himaghna

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip
- Virtual environment

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd lostandfound
```

2. Create and activate virtual environment
```bash
py -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file with:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations
```bash
py manage.py migrate
```

6. Create superuser
```bash
py manage.py createsuperuser
```

7. Run development server
```bash
py manage.py runserver
```

8. Open browser to http://localhost:8000

## Technology Stack
- Django 5.0
- SQLite (development)
- Pillow (image handling)
- PostgreSQL (final database)

## Features
- User registration (Student/Teacher)
- Report found items with photos
- Search and browse items
- Claim items
- Admin dashboard for claim management

## Project Timeline
- MVP: December 1, 2025
- Final: March 1, 2025
```

---

## 🔍 Verify Files Were Created

**In VS Code Explorer, you should see:**
```
lostandfound/
├── .env                 ← Should be here
├── .gitignore          ← Should be here
├── requirements.txt    ← Should be here
├── README.md           ← Should be here
├── manage.py
├── lostandfound/
├── accounts/
├── items/
└── claims/
