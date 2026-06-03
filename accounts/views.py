from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.db.models import Count, Q
from .models import CustomUser, StudentProfile, TeacherProfile
from .emails import (
    send_welcome_email,
    send_teacher_pending_email,
    send_teacher_approved_email,
    send_teacher_rejected_email,
)
from items.models import Item
from claims.models import Claim
from lostandfound.throttle import rate_limit

# Create your views here.
def home(request):
    recent_items = None
    pending_approval_items = None
    slider_items = Item.objects.filter(status__in=['unclaimed', 'rejected']).order_by('-created_at')[:8]

    if request.user.is_authenticated:
        if request.user.is_staff or request.user.user_type in ['teacher', 'admin']:
            pending_approval_items = Item.objects.filter(status='reported').order_by('-created_at')[:5]
            recent_items = Item.objects.filter(status__in=['unclaimed', 'rejected']).order_by('-created_at')[:3]
        else:
            recent_items = Item.objects.filter(status__in=['unclaimed', 'rejected']).order_by('-created_at')[:3]

    return render(request, 'home.html', {
        'recent_items': recent_items,
        'pending_approval_items': pending_approval_items,
        'slider_items': slider_items
    })

@rate_limit(max_requests=5, window_seconds=3600)
def register_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        grade = request.POST.get('grade')
        verification_code = request.POST.get('verification_code', '').strip()

        if verification_code != settings.SCHOOL_VERIFICATION_CODE:
            messages.error(request, 'Invalid school verification code. Please check with your school administrator.')
            return render(request, 'accounts/register_student.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register_student.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different username.')
            return render(request, 'accounts/register_student.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return render(request, 'accounts/register_student.html')

        if StudentProfile.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already registered.')
            return render(request, 'accounts/register_student.html')

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

        login(request, user)
        send_welcome_email(user)
        messages.success(request, f'Welcome, {first_name}! Your account has been created successfully.')
        return redirect('/?login=1')

    return render(request, 'accounts/register_student.html')

@rate_limit(max_requests=5, window_seconds=3600)
def register_teacher(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department', '')
        verification_code = request.POST.get('verification_code', '').strip()

        if verification_code != settings.SCHOOL_VERIFICATION_CODE:
            messages.error(request, 'Invalid school verification code. Please check with your school administrator.')
            return render(request, 'accounts/register_teacher.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register_teacher.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different username.')
            return render(request, 'accounts/register_teacher.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return render(request, 'accounts/register_teacher.html')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type='teacher',
            approval_status='pending',
        )

        TeacherProfile.objects.create(
            user=user,
            department=department
        )

        send_teacher_pending_email(user)
        messages.success(
            request,
            f'Thank you, {first_name}! Your teacher account has been submitted for admin review. '
            'You will receive an email once your account has been approved.'
        )
        return redirect('login')

    return render(request, 'accounts/register_teacher.html')

@rate_limit(max_requests=10, window_seconds=300)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not (user.is_staff or user.is_superuser or user.user_type == 'admin'):
                if user.approval_status == 'pending':
                    messages.warning(request, 'Your account is pending approval. Please wait for an administrator to approve your registration. If you have questions, contact the school office.')
                    return render(request, 'accounts/login.html')
                elif user.approval_status == 'rejected':
                    messages.error(request, 'Your account registration was rejected. Please contact the school office or a system administrator for assistance.')
                    return render(request, 'accounts/login.html')

            login(request, user)

            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            else:
                return redirect('/?login=1')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def pending_users(request):
    if not (request.user.is_staff or request.user.user_type == 'admin'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

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

            if user_to_approve.user_type == 'teacher':
                send_teacher_approved_email(user_to_approve)
            else:
                send_welcome_email(user_to_approve)

            messages.success(request, f'User {user_to_approve.username} has been approved.')

        elif action == 'reject':
            user_to_approve.approval_status = 'rejected'
            user_to_approve.save()

            if user_to_approve.user_type == 'teacher':
                send_teacher_rejected_email(user_to_approve)

            messages.success(request, f'User {user_to_approve.username} has been rejected.')

        return redirect('pending_users')

    return render(request, 'accounts/approve_user.html', {'user_to_approve': user_to_approve})


@login_required
def analytics(request):
    if not (request.user.is_staff or request.user.user_type in ['admin', 'teacher']):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    # --- Item stats ---
    total_items = Item.objects.count()
    items_by_status = {
        'reported':  Item.objects.filter(status='reported').count(),
        'unclaimed': Item.objects.filter(status='unclaimed').count(),
        'verified':  Item.objects.filter(status='verified').count(),
        'returned':  Item.objects.filter(status='returned').count(),
        'discarded': Item.objects.filter(status='discarded').count(),
        'rejected':  Item.objects.filter(status='rejected').count(),
    }

    # Recovery rate = items returned / all items that reached unclaimed or beyond
    processed = Item.objects.exclude(status='reported').count()
    returned  = items_by_status['returned']
    recovery_rate = round((returned / processed * 100) if processed > 0 else 0, 1)

    # Items by category
    items_by_category = (
        Item.objects
        .values('category')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    category_display = dict(Item.CATEGORY_CHOICES)
    items_by_category = [
        {'label': category_display.get(row['category'], row['category']), 'count': row['total']}
        for row in items_by_category
    ]

    # Long-sitting unclaimed items (30+ days)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    stale_items = Item.objects.filter(
        status__in=['unclaimed', 'rejected'],
        created_at__lte=thirty_days_ago
    ).count()

    # Items reported in last 7 / 30 days
    seven_days_ago  = timezone.now() - timezone.timedelta(days=7)
    new_items_7d    = Item.objects.filter(created_at__gte=seven_days_ago).count()
    new_items_30d   = Item.objects.filter(created_at__gte=thirty_days_ago).count()

    # --- Claim stats ---
    total_claims = Claim.objects.count()
    claims_by_status = {
        'pending':   Claim.objects.filter(status='pending').count(),
        'approved':  Claim.objects.filter(status='approved').count(),
        'rejected':  Claim.objects.filter(status='rejected').count(),
        'completed': Claim.objects.filter(status='completed').count(),
    }
    claim_approval_rate = round(
        (claims_by_status['approved'] + claims_by_status['completed']) /
        total_claims * 100 if total_claims > 0 else 0, 1
    )

    # --- User stats ---
    total_users    = CustomUser.objects.exclude(user_type='admin').count()
    total_students = CustomUser.objects.filter(user_type='student', approval_status='approved').count()
    total_teachers = CustomUser.objects.filter(user_type='teacher', approval_status='approved').count()
    pending_users_count = CustomUser.objects.filter(approval_status='pending').count()

    # Top reporters (students who submitted the most items)
    top_reporters = (
        CustomUser.objects
        .annotate(item_count=Count('submitted_items'))
        .filter(item_count__gt=0)
        .order_by('-item_count')[:5]
    )

    context = {
        # Items
        'total_items':        total_items,
        'items_by_status':    items_by_status,
        'recovery_rate':      recovery_rate,
        'items_by_category':  items_by_category,
        'stale_items':        stale_items,
        'new_items_7d':       new_items_7d,
        'new_items_30d':      new_items_30d,
        # Claims
        'total_claims':       total_claims,
        'claims_by_status':   claims_by_status,
        'claim_approval_rate': claim_approval_rate,
        # Users
        'total_users':        total_users,
        'total_students':     total_students,
        'total_teachers':     total_teachers,
        'pending_users_count': pending_users_count,
        'top_reporters':      top_reporters,
    }
    return render(request, 'accounts/analytics.html', context)