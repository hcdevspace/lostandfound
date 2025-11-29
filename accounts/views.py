from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser, StudentProfile, TeacherProfile

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register_student(request):
    if request.method == 'POST':
        #Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        grade = request.POST.get('grade')

        # Validate username doesn't already exist
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different username.')
            return render(request, 'accounts/register_student.html')

        # Validate email doesn't already exist
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return render(request, 'accounts/register_student.html')

        # Validate student ID doesn't already exist
        if StudentProfile.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already registered.')
            return render(request, 'accounts/register_student.html')

        #Creates user, .create_user() method hashes password
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type='student'
        )

        StudentProfile.objects.create(
            user=user,
            student_id=student_id,
            grade=grade
        )

        messages.success(request, 'Registration Successful! Please login now.')
        return redirect('login')

    return render(request, 'accounts/register_student.html')

def register_teacher(request):
    if request.method == 'POST':
        #Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department', '')

        # Validate username doesn't already exist
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different username.')
            return render(request, 'accounts/register_teacher.html')

        # Validate email doesn't already exist
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return render(request, 'accounts/register_teacher.html')

        #Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type='teacher'
        )

        TeacherProfile.objects.create(
            user=user,
            department=department
        )

        messages.success(request, 'Registration Successful! Please login now.')
        return redirect('login')

    return render(request, 'accounts/register_teacher.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None: # Valid credentials entered
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('home')
        else: # Invalid credentials
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')