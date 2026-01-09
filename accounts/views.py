from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser, StudentProfile, TeacherProfile
from items.models import Item

# Create your views here.
def home(request):
    # Get recent items if user is logged in
    recent_items = None
    pending_approval_items = None
    slider_items = Item.objects.filter(status__in=['unclaimed', 'rejected']).order_by('-created_at')[:8]

    if request.user.is_authenticated:
        # For admins/teachers, show items pending approval
        if request.user.is_staff or request.user.user_type in ['teacher', 'admin']:
            pending_approval_items = Item.objects.filter(status='reported').order_by('-created_at')[:5]
            recent_items = Item.objects.filter(status__in=['unclaimed', 'rejected']).order_by('-created_at')[:3]
        else:
            # For students, show unclaimed items
            recent_items = Item.objects.filter(status__in=['unclaimed', 'rejected']).order_by('-created_at')[:3]

    return render(request, 'home.html', {
        'recent_items': recent_items,
        'pending_approval_items': pending_approval_items,
        'slider_items': slider_items
    })

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

        messages.success(request, 'Registration submitted successfully! Your account is pending approval. An administrator will review your registration soon.')
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

        messages.success(request, 'Registration submitted successfully! Your account is pending approval. An administrator will review your registration soon.')
        return redirect('login')

    return render(request, 'accounts/register_teacher.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None: # Valid credentials entered
            # Check if user is approved (skip check for admins and superusers)
            if not (user.is_staff or user.is_superuser or user.user_type == 'admin'):
                if user.approval_status == 'pending':
                    messages.warning(request, 'Your account is pending approval. Please wait for an administrator to approve your registration.')
                    return render(request, 'accounts/login.html')
                elif user.approval_status == 'rejected':
                    messages.error(request, 'Your account registration was rejected. Please contact an administrator for more information.')
                    return render(request, 'accounts/login.html')

            # User is approved or is admin, allow login
            login(request, user)

            # Redirect to the 'next' parameter if provided, otherwise go to home
            next_url = request.GET.get('next') or request.POST.get('next')

            if next_url:
                return redirect(next_url)
            else:
                # Add login parameter when redirecting to home to show welcome message
                return redirect('/?login=1')
        else: # Invalid credentials
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def pending_users(request):
    # Only admins can access this page
    if not (request.user.is_staff or request.user.user_type == 'admin'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    # Get filter status
    status_filter = request.GET.get('status', 'pending')

    if status_filter == 'all':
        users = CustomUser.objects.exclude(user_type='admin').order_by('-date_joined')
    else:
        users = CustomUser.objects.filter(approval_status=status_filter).exclude(user_type='admin').order_by('-date_joined')

    return render(request, 'accounts/pending_users.html', {
        'users': users,
        'current_filter': status_filter
    })

@login_required
def approve_user(request, user_id):
    # Only admins can approve users
    if not (request.user.is_staff or request.user.user_type == 'admin'):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')

    user_to_approve = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            user_to_approve.approval_status = 'approved'
            user_to_approve.approved_by = request.user
            user_to_approve.approval_date = timezone.now()
            user_to_approve.save()
            messages.success(request, f'User {user_to_approve.username} has been approved.')
        elif action == 'reject':
            user_to_approve.approval_status = 'rejected'
            user_to_approve.save()
            messages.success(request, f'User {user_to_approve.username} has been rejected.')

        return redirect('pending_users')

    return render(request, 'accounts/approve_user.html', {'user_to_approve': user_to_approve})