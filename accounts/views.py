from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .models import CustomUser, StudentProfile, TeacherProfile
from .emails import send_welcome_email
from items.models import Item
from lostandfound.throttle import rate_limit

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

@rate_limit(max_requests=5, window_seconds=3600)  # 5 registration attempts per hour
def register_student(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        grade = request.POST.get('grade')
        verification_code = request.POST.get('verification_code', '').strip()

        # Validate verification code first
        if verification_code != settings.SCHOOL_VERIFICATION_CODE:
            messages.error(request, 'Invalid school verification code. Please check with your school administrator.')
            return render(request, 'accounts/register_student.html')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register_student.html')

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

        # Verification code passed — create user and approve immediately
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type='student',
            approval_status='approved',
            approval_date=timezone.now(),
        )

        StudentProfile.objects.create(
            user=user,
            student_id=student_id,
            grade=grade
        )

        # Log the user in immediately — no waiting for admin
        login(request, user)
        send_welcome_email(user)
        messages.success(request, f'Welcome, {first_name}! Your account has been created successfully.')
        return redirect('/?login=1')

    return render(request, 'accounts/register_student.html')

@rate_limit(max_requests=5, window_seconds=3600)  # 5 registration attempts per hour
def register_teacher(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department', '')
        verification_code = request.POST.get('verification_code', '').strip()

        # Validate verification code first
        if verification_code != settings.SCHOOL_VERIFICATION_CODE:
            messages.error(request, 'Invalid school verification code. Please check with your school administrator.')
            return render(request, 'accounts/register_teacher.html')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register_teacher.html')

        # Validate username doesn't already exist
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different username.')
            return render(request, 'accounts/register_teacher.html')

        # Validate email doesn't already exist
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return render(request, 'accounts/register_teacher.html')

        # Verification code passed — create user and approve immediately
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type='teacher',
            approval_status='approved',
            approval_date=timezone.now(),
        )

        TeacherProfile.objects.create(
            user=user,
            department=department
        )

        # Log the user in immediately — no waiting for admin
        login(request, user)
        send_welcome_email(user)
        messages.success(request, f'Welcome, {first_name}! Your account has been created successfully.')
        return redirect('/?login=1')

    return render(request, 'accounts/register_teacher.html')

@rate_limit(max_requests=10, window_seconds=300)  # 10 login attempts per 5 minutes
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None: # Valid credentials entered
            # Check if user is approved (skip check for admins and superusers)
            if not (user.is_staff or user.is_superuser or user.user_type == 'admin'):
                if user.approval_status == 'pending':
                    messages.warning(request, 'Your account is pending approval. Please wait for an administrator to approve your registration. If you have questions, contact the school office.')
                    return render(request, 'accounts/login.html')
                elif user.approval_status == 'rejected':
                    messages.error(request, 'Your account registration was rejected. Please contact the school office or a system administrator for assistance.')
                    return render(request, 'accounts/login.html')

            # User is approved or is admin, allow login
            login(request, user)

            # Redirect to the 'next' parameter if provided, otherwise go to home
            next_url = request.GET.get('next') or request.POST.get('next')

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
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