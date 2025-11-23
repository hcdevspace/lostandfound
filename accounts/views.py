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

        #Create user
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

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')