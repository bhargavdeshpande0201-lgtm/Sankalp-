from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Complaint, Comment, EmailVerificationToken, PasswordResetToken
from .forms import ComplaintForm, CommentForm, PasswordResetRequestForm, PasswordResetForm
from django.db.models import Q, Count
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import secrets


# ==================== HOME ====================
def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    
    stats = {
        'total_complaints': Complaint.objects.count(),
        'pending_complaints': Complaint.objects.filter(status='Pending').count(),
        'in_progress': Complaint.objects.filter(status='In Progress').count(),
        'resolved': Complaint.objects.filter(status='Resolved').count(),
    }
    return render(request, 'index.html', {'stats': stats})


# ==================== AUTHENTICATION ====================
@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        role = request.POST.get('role', 'student')
        
        # Validation
        if not all([username, email, password1, password2]):
            messages.error(request, 'All fields are required')
            return redirect('register')
        
        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters')
            return redirect('register')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return redirect('register')
        
        # Check password strength
        if not any(char.isdigit() for char in password1):
            messages.error(request, 'Password must contain at least one number')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.is_active = False  # User inactive until email verified
        
        if role == 'teacher':
            user.is_staff = True
        
        user.save()
        
        # Generate email verification token
        token = EmailVerificationToken.generate_token()
        EmailVerificationToken.objects.create(user=user, token=token)
        
        # Send verification email
        verification_url = request.build_absolute_uri(
            reverse('verify_email', args=[user.id, token])
        )
        
        subject = 'Verify Your Email - SANKALP Campus Management'
        message = f"""
Hello {username},

Welcome to SANKALP Campus Management System!

Please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

If you didn't create this account, please ignore this email.

Best regards,
SANKALP Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(
                request, 
                f'Account created successfully! A verification email has been sent to {email}. Please check your inbox and verify your email to login.'
            )
        except Exception as e:
            messages.warning(
                request,
                f'Account created but email could not be sent: {str(e)}. Please contact support for manual verification.'
            )
        
        return redirect('login')
    
    return render(request, 'register.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Secure login view with role-based authentication.
    Supports: Student, Teacher/Staff, and Admin login
    """
    # Redirect already authenticated users
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'student')
        
        # Validation
        if not username or not password:
            messages.error(request, 'Username and password are required')
            return render(request, 'login.html', {'role': role})
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if email is verified
            if not user.is_active:
                messages.error(
                    request,
                    'Your email address is not verified. Please check your inbox for the verification link.'
                )
                return render(request, 'login.html', {'role': role, 'unverified_email': user.email})
            
            # Role-based access control
            if role == 'admin':
                # Only superuser can login as admin
                if not user.is_superuser:
                    messages.error(
                        request, 
                        'Invalid credentials for Admin login. Contact system administrator if you believe this is a mistake.'
                    )
                    return render(request, 'login.html', {'role': role})
                    
            elif role == 'teacher':
                # Only staff can login as teacher
                if not user.is_staff:
                    messages.error(
                        request, 
                        'Invalid credentials for Teacher/Staff login.'
                    )
                    return render(request, 'login.html', {'role': role})
                    
            elif role == 'student':
                # Regular users can be students
                if user.is_superuser and user.is_staff:
                    # Admins should use admin login
                    messages.warning(
                        request, 
                        'Admin account detected. Please use Admin login or contact support.'
                    )
                    return render(request, 'login.html', {'role': role})
            
            # Login successful
            login(request, user)
            
            # Create welcome message with user info
            user_info = user.get_full_name() if user.get_full_name() else user.username
            user_role = 'Admin/Superuser' if user.is_superuser else 'Staff/Teacher' if user.is_staff else 'Student'
            messages.success(request, f'Welcome {user_info}! ({user_role})')
            
            # Redirect based on user role
            if user.is_superuser or (user.is_staff and role == 'admin'):
                return redirect('admin_dashboard')
            elif user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(
                request, 
                'Invalid username or password. Please try again or contact support if you need help.'
            )
            return render(request, 'login.html', {'role': role})
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('index')


# ==================== EMAIL VERIFICATION ====================
def verify_email(request, user_id, token):
    """Verify user email address using token from email link"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('login')
    
    try:
        verification = EmailVerificationToken.objects.get(user=user, token=token)
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid or already used verification link.')
        return redirect('login')
    
    if not verification.is_valid():
        verification.delete()
        messages.error(request, 'Verification link has expired. Please register again.')
        return redirect('register')
    
    # Activate user and delete token
    user.is_active = True
    user.save()
    verification.delete()
    
    return render(request, 'email_verified.html', {'user': user})


def resend_verification(request):
    """Resend verification email"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email, is_active=False)
            
            # Delete old token if exists
            EmailVerificationToken.objects.filter(user=user).delete()
            
            # Create new token
            token = EmailVerificationToken.generate_token()
            EmailVerificationToken.objects.create(user=user, token=token)
            
            verification_url = request.build_absolute_uri(
                reverse('verify_email', args=[user.id, token])
            )
            
            try:
                send_mail(
                    'Verify Your Email - SANKALP Campus Management',
                    f'Hello {user.username},\n\nClick the link below to verify your email:\n\n{verification_url}\n\nThis link expires in 24 hours.\n\nSANKALP Team',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f'Verification email resent to {email}. Please check your inbox.')
            except Exception as e:
                messages.error(request, f'Could not send email: {str(e)}')
        except User.DoesNotExist:
            # Don't reveal if email exists or not
            messages.success(request, f'If {email} is registered and unverified, a new link has been sent.')
    
    return redirect('login')


# ==================== PASSWORD RESET ====================
@require_http_methods(["GET", "POST"])
def forgot_password(request):
    """Send password reset email with secure DB-stored token"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Delete any existing unused tokens for this user
            PasswordResetToken.objects.filter(user=user, used=False).delete()
            
            # Create new DB-stored token
            token = PasswordResetToken.generate_token()
            PasswordResetToken.objects.create(user=user, token=token)
            
            reset_url = request.build_absolute_uri(
                reverse('reset_password', args=[user.id, token])
            )
            
            subject = 'Password Reset Request - SANKALP Campus Management'
            message = f"""Hello {user.first_name or user.username},

We received a request to reset your SANKALP account password.

Click the link below to reset your password:

{reset_url}

This link will expire in 1 hour.

If you did not request a password reset, please ignore this email. Your password will remain unchanged.

Best regards,
SANKALP Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    f'Password reset link sent to {email}. Please check your inbox (and spam folder).'
                )
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}. Please try again later.')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'forgot_password.html', {'form': form})


@require_http_methods(["GET", "POST"])
def reset_password(request, user_id, token):
    """Reset password using secure DB-stored token"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid reset link.')
        return redirect('login')
    
    # Verify token from DB
    try:
        reset_token = PasswordResetToken.objects.get(user=user, token=token)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid or already used reset link.')
        return redirect('login')
    
    if not reset_token.is_valid():
        reset_token.delete()
        messages.error(request, 'Reset link has expired. Please request a new one.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            # Mark token as used
            reset_token.used = True
            reset_token.save()
            
            messages.success(request, 'Password reset successfully! You can now login with your new password.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    
    return render(request, 'reset_password.html', {'form': form, 'user': user})


# ==================== STUDENT DASHBOARD ====================
@login_required(login_url='login')
def dashboard(request):
    if request.user.is_staff and not request.user.is_superuser:
        return redirect('admin_dashboard')
    
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'complaints': complaints,
        'total_complaints': complaints.count(),
        'pending_count': complaints.filter(status='Pending').count(),
        'in_progress_count': complaints.filter(status='In Progress').count(),
        'resolved_count': complaints.filter(status='Resolved').count(),
    }
    
    return render(request, 'dashboard.html', context)


# ==================== COMPLAINT MANAGEMENT ====================
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def add_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.status = 'Pending'
            complaint.save()
            
            messages.success(request, 'Complaint submitted successfully!')
            return redirect('complaint_detail', pk=complaint.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ComplaintForm()
    
    return render(request, 'add_complaint.html', {'form': form})


@login_required(login_url='login')
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Permission check
    is_owner = complaint.user == request.user
    is_staff = request.user.is_staff
    
    if not is_owner and not is_staff:
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')
    
    comments = complaint.comments.all().order_by('-created_at')
    
    context = {
        'complaint': complaint,
        'comments': comments,
        'is_owner': is_owner,
    }
    
    return render(request, 'complaint_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_comment(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    is_owner = complaint.user == request.user
    is_staff = request.user.is_staff
    
    if not is_owner and not is_staff:
        messages.error(request, 'Unauthorized')
        return redirect('dashboard')
    
    text = request.POST.get('text', '').strip()
    
    if not text:
        messages.error(request, 'Comment cannot be empty')
        return redirect('complaint_detail', pk=pk)
    
    Comment.objects.create(
        complaint=complaint,
        user=request.user,
        text=text,
        is_staff=is_staff
    )
    
    messages.success(request, 'Comment added successfully')
    return redirect('complaint_detail', pk=pk)


@login_required(login_url='login')
def delete_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    is_owner = complaint.user == request.user
    is_admin = request.user.is_staff or request.user.is_superuser

    if not is_owner and not is_admin:
        messages.error(request, 'You do not have permission to delete this complaint.')
        return redirect('dashboard')

    if is_owner and not is_admin and complaint.status in ['Resolved', 'Rejected']:
        messages.error(request, 'You cannot delete this complaint as it has been processed. Contact an administrator.')
        return redirect('complaint_detail', pk=pk)

    if request.method == 'POST':
        complaint_title = complaint.title
        complaint_id = complaint.id
        complaint.delete()
        messages.success(request, f'Complaint "{complaint_title}" (ID: {complaint_id}) has been deleted successfully.')
        if is_admin:
            return redirect('admin_dashboard')
        return redirect('dashboard')

    return render(request, 'delete_complaint.html', {'complaint': complaint})


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission')
        return redirect('dashboard')
    
    new_status = request.POST.get('status')
    comment_text = request.POST.get('comment', '')
    
    if new_status in ['Pending', 'In Progress', 'Resolved', 'Rejected']:
        complaint.status = new_status
        complaint.save()
        
        if comment_text:
            Comment.objects.create(
                complaint=complaint,
                user=request.user,
                text=comment_text,
                is_staff=True
            )
        
        messages.success(request, f'Complaint status updated to {new_status}')
    else:
        messages.error(request, 'Invalid status')
    
    return redirect('complaint_detail', pk=pk)


# ==================== USER PROFILE ====================
@login_required(login_url='login')
def profile(request):
    user = request.user
    complaints = Complaint.objects.filter(user=user).order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'total_complaints': Complaint.objects.filter(user=user).count(),
        'resolved_count': Complaint.objects.filter(user=user, status='Resolved').count(),
        'pending_count': Complaint.objects.filter(user=user, status='Pending').count(),
        'recent_complaints': complaints,
    }
    
    return render(request, 'profile.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_profile(request):
    user = request.user
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    
    user.save()
    messages.success(request, 'Profile updated successfully')
    return redirect('profile')


@login_required(login_url='login')
@require_http_methods(["POST"])
def change_password(request):
    user = request.user
    old_password = request.POST.get('old_password', '')
    new_password1 = request.POST.get('new_password1', '')
    new_password2 = request.POST.get('new_password2', '')
    
    if not user.check_password(old_password):
        messages.error(request, 'Current password is incorrect')
        return redirect('profile')
    
    if new_password1 != new_password2:
        messages.error(request, 'New passwords do not match')
        return redirect('profile')
    
    if len(new_password1) < 8:
        messages.error(request, 'Password must be at least 8 characters')
        return redirect('profile')
    
    user.set_password(new_password1)
    user.save()
    update_session_auth_hash(request, user)
    
    messages.success(request, 'Password changed successfully')
    return redirect('profile')


# ==================== ADMIN DASHBOARD ====================
@login_required(login_url='login')
def admin_dashboard(request):
    """
    Admin dashboard with comprehensive complaint management and statistics.
    Restricted to staff and superuser accounts only.
    """
    # Permission check: Only staff and superusers can access
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    # Get all complaints with filtering
    complaints_query = Complaint.objects.all()
    
    # Optional filtering
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    priority_filter = request.GET.get('priority', '')
    
    if status_filter:
        complaints_query = complaints_query.filter(status=status_filter)
    if category_filter:
        complaints_query = complaints_query.filter(category=category_filter)
    if priority_filter:
        complaints_query = complaints_query.filter(priority=priority_filter)
    
    # Order by most recent
    complaints = complaints_query.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(complaints, 15)  # 15 complaints per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_complaints = Complaint.objects.count()
    pending = Complaint.objects.filter(status='Pending').count()
    in_progress = Complaint.objects.filter(status='In Progress').count()
    resolved = Complaint.objects.filter(status='Resolved').count()
    rejected = Complaint.objects.filter(status='Rejected').count()
    
    # High priority complaints
    high_priority = Complaint.objects.filter(priority='high').count()
    
    # Resolution rate
    resolution_rate = int((resolved / total_complaints * 100) if total_complaints > 0 else 0)
    
    # Category breakdown
    category_stats = Complaint.objects.values('category').annotate(count=Count('id'))

    # Category individual counts for sidebar
    waste_count = Complaint.objects.filter(category='Waste').count()
    parking_count = Complaint.objects.filter(category='Parking').count()
    infra_count = Complaint.objects.filter(category='Infrastructure').count()
    security_count = Complaint.objects.filter(category='Security').count()

    context = {
        'page_obj': page_obj,
        'complaints': page_obj.object_list,
        'total_complaints': total_complaints,
        'pending_count': pending,
        'in_progress_count': in_progress,
        'resolved_count': resolved,
        'rejected_count': rejected,
        'high_priority_count': high_priority,
        'users_count': User.objects.count(),
        'resolution_rate': resolution_rate,
        'category_stats': category_stats,
        'waste_count': waste_count,
        'parking_count': parking_count,
        'infra_count': infra_count,
        'security_count': security_count,
        # Filters
        'status_filter': status_filter,
        'category_filter': category_filter,
        'priority_filter': priority_filter,
        # Choices for filter dropdowns
        'status_choices': Complaint.STATUS_CHOICES,
        'category_choices': Complaint.CATEGORY_CHOICES,
        'priority_choices': Complaint.PRIORITY_CHOICES,
    }
    
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='login')
def admin_edit_complaint(request, pk):
    """
    Edit complaint details - admin only.
    Allows changing status, priority, and adding staff comments.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status', '').strip()
        priority = request.POST.get('priority', '').strip()
        comment_text = request.POST.get('comment', '').strip()
        
        # Validate status
        valid_statuses = [choice[0] for choice in Complaint.STATUS_CHOICES]
        valid_priorities = [choice[0] for choice in Complaint.PRIORITY_CHOICES]
        
        # Update status if valid
        if status and status in valid_statuses:
            old_status = complaint.status
            complaint.status = status
            
            # Log status change as comment
            if old_status != status and not comment_text:
                comment_text = f"Status changed from {old_status} to {status}"
        
        # Update priority if valid
        if priority and priority in valid_priorities:
            complaint.priority = priority
        
        # Save complaint changes
        complaint.save()
        
        # Add comment from staff if provided
        if comment_text:
            Comment.objects.create(
                complaint=complaint,
                user=request.user,
                text=comment_text,
                is_staff=True
            )
        
        messages.success(request, 'Complaint updated successfully')
        return redirect('admin_dashboard')
    
    comments = complaint.comments.all().order_by('-created_at')
    
    context = {
        'complaint': complaint,
        'comments': comments,
        'status_choices': Complaint.STATUS_CHOICES,
        'priority_choices': Complaint.PRIORITY_CHOICES,
    }
    
    return render(request, 'admin_edit_complaint.html', context)


# ==================== SEARCH & FILTERS ====================
@login_required(login_url='login')
def search_complaints(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    
    complaints = Complaint.objects.filter(user=request.user)
    
    if query:
        complaints = complaints.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )
    
    if category:
        complaints = complaints.filter(category=category)
    
    if status:
        complaints = complaints.filter(status=status)
    
    context = {
        'complaints': complaints,
        'query': query,
        'category': category,
        'status': status,
    }
    
    return render(request, 'search_complaints.html', context)


# ==================== NEW FEATURES ====================
@login_required(login_url='login')
def assign_complaint(request, pk):
    """
    Assign a complaint to staff member - admin only.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        assigned_to_id = request.POST.get('assigned_to', '')
        comment_text = request.POST.get('comment', '').strip()
        
        if assigned_to_id:
            try:
                staff_user = User.objects.get(id=assigned_to_id, is_staff=True)
                complaint.assigned_to = staff_user
                complaint.save()
                
                # Add comment about assignment
                if not comment_text:
                    comment_text = f"Assigned to {staff_user.get_full_name() or staff_user.username}"
                
                Comment.objects.create(
                    complaint=complaint,
                    user=request.user,
                    text=comment_text,
                    is_staff=True
                )
                
                messages.success(request, f'Complaint assigned to {staff_user.get_full_name() or staff_user.username}')
                return redirect('admin_dashboard')
            except User.DoesNotExist:
                messages.error(request, 'Invalid staff member selected')
        else:
            messages.error(request, 'Please select a staff member')
    
    # Get all staff members
    staff_members = User.objects.filter(is_staff=True)
    
    context = {
        'complaint': complaint,
        'staff_members': staff_members,
    }
    
    return render(request, 'assign_complaint.html', context)


@login_required(login_url='login')
def admin_manage_users(request):
    """
    Admin page to manage all users.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    
    # Filter by user type
    user_type = request.GET.get('type', '')
    if user_type == 'staff':
        users = users.filter(is_staff=True)
    elif user_type == 'students':
        users = users.filter(is_staff=False, is_superuser=False)
    elif user_type == 'admin':
        users = users.filter(is_superuser=True)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'users': page_obj.object_list,
        'total_users': User.objects.count(),
        'staff_count': User.objects.filter(is_staff=True).count(),
        'student_count': User.objects.filter(is_staff=False, is_superuser=False).count(),
        'admin_count': User.objects.filter(is_superuser=True).count(),
        'user_type': user_type,
    }
    
    return render(request, 'admin_manage_users.html', context)


@login_required(login_url='login')
def admin_reports(request):
    """
    Generate reports on complaints and statistics.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    # Summary statistics
    total_complaints = Complaint.objects.count()
    pending = Complaint.objects.filter(status='Pending').count()
    in_progress = Complaint.objects.filter(status='In Progress').count()
    resolved = Complaint.objects.filter(status='Resolved').count()
    rejected = Complaint.objects.filter(status='Rejected').count()
    
    # Category breakdown
    category_stats = []
    for category, name in Complaint.CATEGORY_CHOICES:
        count = Complaint.objects.filter(category=category).count()
        category_stats.append({
            'name': name,
            'count': count,
            'percentage': int((count / total_complaints * 100) if total_complaints > 0 else 0)
        })
    
    # Priority breakdown
    priority_stats = []
    for priority, name in Complaint.PRIORITY_CHOICES:
        count = Complaint.objects.filter(priority=priority).count()
        priority_stats.append({
            'name': name,
            'count': count,
            'percentage': int((count / total_complaints * 100) if total_complaints > 0 else 0)
        })
    
    # Top reporters
    top_reporters = User.objects.annotate(complaint_count=Count('complaints')).order_by('-complaint_count')[:5]
    
    context = {
        'total_complaints': total_complaints,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'rejected': rejected,
        'resolution_rate': int((resolved / total_complaints * 100) if total_complaints > 0 else 0),
        'category_stats': category_stats,
        'priority_stats': priority_stats,
        'top_reporters': top_reporters,
    }
    
    return render(request, 'admin_reports.html', context)


@login_required(login_url='login')
def admin_recent_activity(request):
    """
    Display recent activity in the system.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    # Get recent complaints
    recent_complaints = Complaint.objects.all().order_by('-created_at')[:10]
    
    # Get recent comments
    recent_comments = Comment.objects.all().order_by('-created_at')[:15]
    
    context = {
        'recent_complaints': recent_complaints,
        'recent_comments': recent_comments,
    }
    
    return render(request, 'admin_recent_activity.html', context)


def terms_and_conditions(request):
    """
    Terms and Conditions page.
    """
    return render(request, 'terms_and_conditions.html')


def contact_support(request):
    """
    Contact and Support Information page.
    """
    support_contacts = [
        {
            'name': 'Bhargav Deshpande',
            'role': 'Support Head',
            'email': 'bhargav.deshpande@sankalp.edu.in',
            'mobile': '+91-98765-43210',
            'availability': 'Monday - Friday, 9 AM - 6 PM'
        },
        {
            'name': 'Ved Derkar',
            'role': 'Technical Support',
            'email': 'ved.derkar@sankalp.edu.in',
            'mobile': '+91-91234-56789',
            'availability': 'Monday - Friday, 9 AM - 5 PM'
        }
    ]
    
    context = {
        'support_contacts': support_contacts,
    }
    
    return render(request, 'contact_support.html', context)
