# ReFind - Lost and Found School Management System

## Project Description
A Django web application to help students and staff report found items, search for lost belongings, and manage the claim process efficiently.

## Technologies Used
- Django 5.2.8
- Python 3.14
- PostgreSQL

## Setup Instructions

### Installation

1. Clone the repository
```bash
git clone https://www.github.com/hcdevspace/lostandfound
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

4. Create a `.env` file in the project root with the following:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

SCHOOL_VERIFICATION_CODE=SCHOOL2026
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password
DEFAULT_FROM_EMAIL=Lost & Found <your_gmail@gmail.com>

DB_ENGINE=postgres
DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=dbpassword
DB_HOST=localhost
DB_PORT=5432
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

### Running on Network (Access from Other Devices)

To allow access from other devices on your local network:

1. Find your computer's local IP address:
   - **Windows**: Open Command Prompt and run `ipconfig`
   - Look for "IPv4 Address" (e.g., 192.168.1.100)
   - **Mac/Linux**: Run `ifconfig` or `ip addr`

2. Run the development server on all network interfaces:
```bash
py manage.py runserver 0.0.0.0:8000
```

3. Access the application from other devices:
   - On the same computer: http://localhost:8000
   - From other devices on the network: http://YOUR_IP_ADDRESS:8000
   - Example: http://192.168.1.100:8000

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

## Team Members
- Harshit, Aaryan, Himaghna


