import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostandfound.settings')
django.setup()

from accounts.models import CustomUser, StudentProfile, TeacherProfile

pending_users = [
    {
        'username': 'emma.johnson',
        'first_name': 'Emma',
        'last_name': 'Johnson',
        'email': 'emma.johnson@school.edu',
        'user_type': 'student',
        'student_id': '100421',
        'grade': 10,
    },
    {
        'username': 'liam.patel',
        'first_name': 'Liam',
        'last_name': 'Patel',
        'email': 'liam.patel@school.edu',
        'user_type': 'student',
        'student_id': '100422',
        'grade': 11,
    },
    {
        'username': 'sofia.chen',
        'first_name': 'Sofia',
        'last_name': 'Chen',
        'email': 'sofia.chen@school.edu',
        'user_type': 'student',
        'student_id': '100423',
        'grade': 9,
    },
    {
        'username': 'mr.davis',
        'first_name': 'David',
        'last_name': 'Davis',
        'email': 'davis@school.edu',
        'user_type': 'teacher',
        'department': 'Mathematics',
    },
    {
        'username': 'ms.nguyen',
        'first_name': 'Linda',
        'last_name': 'Nguyen',
        'email': 'nguyen@school.edu',
        'user_type': 'teacher',
        'department': 'English',
    },
]

spam_users = [
    {
        'username': 'xXx_user_xXx',
        'first_name': 'asdf',
        'last_name': 'qwerty',
        'email': 'freeprize123@tempmail.com',
        'user_type': 'student',
        'student_id': '000000',
        'grade': 9,
        'spam_score': 85,
        'spam_reasons': 'Disposable email domain; Keyboard mash name; Generic filler username',
        'registration_ip': '192.168.1.50',
    },
    {
        'username': 'aaaaabbbbb',
        'first_name': 'aaaaaa',
        'last_name': 'bbbbbb',
        'email': 'win.money.now@mailinator.com',
        'user_type': 'student',
        'student_id': '111111',
        'grade': 9,
        'spam_score': 92,
        'spam_reasons': 'Disposable email domain; Repeated character name; Suspicious username pattern',
        'registration_ip': '192.168.1.50',
    },
    {
        'username': 'test.user.99',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser99@guerrillamail.com',
        'user_type': 'student',
        'student_id': '999999',
        'grade': 9,
        'spam_score': 78,
        'spam_reasons': 'Disposable email domain; Generic test name; Same IP as other flagged registrations',
        'registration_ip': '192.168.1.50',
    },
]

for data in pending_users:
    if CustomUser.objects.filter(username=data['username']).exists():
        print(f"Skipped (exists): {data['username']}")
        continue

    user = CustomUser.objects.create_user(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password='demo1234',
        user_type=data['user_type'],
        approval_status='pending',
    )

    if data['user_type'] == 'student':
        StudentProfile.objects.create(
            user=user,
            student_id=data['student_id'],
            grade=data['grade'],
        )
    elif data['user_type'] == 'teacher':
        TeacherProfile.objects.create(
            user=user,
            department=data['department'],
        )

    print(f"Created pending: {user.username}")

for data in spam_users:
    if CustomUser.objects.filter(username=data['username']).exists():
        print(f"Skipped (exists): {data['username']}")
        continue

    user = CustomUser.objects.create_user(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password='demo1234',
        user_type=data['user_type'],
        approval_status='pending',
        spam_score=data['spam_score'],
        spam_reasons=data['spam_reasons'],
        registration_ip=data['registration_ip'],
    )

    StudentProfile.objects.create(
        user=user,
        student_id=data['student_id'],
        grade=data['grade'],
    )

    print(f"Created spam: {user.username}")

print("Done.")
