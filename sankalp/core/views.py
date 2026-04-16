from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Complaint, Comment
from .forms import ComplaintForm, CommentForm
from django.db.models import Q, Count


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
        
        if role == 'teacher':
            user.is_staff = True
            user.save()
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'student')
        
        if not username or not password:
            messages.error(request, 'Username and password are required')
            return render(request, 'login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if role == 'admin':
                if not user.is_superuser:
                    messages.error(request, 'Invalid credentials for Admin login')
                    return render(request, 'login.html')
            elif role == 'teacher':
                if not user.is_staff:
                    messages.error(request, 'Invalid credentials for Teacher/Staff login')
                    return render(request, 'login.html')
            
            login(request, user)
            messages.success(request, f'Welcome {user.get_full_name() or user.username}!')
            
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('index')


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
    
    if complaint.user != request.user and not request.user.is_staff:
        messages.error(request, 'You cannot delete this complaint')
        return redirect('dashboard')
    
    complaint.delete()
    messages.success(request, 'Complaint deleted successfully')
    return redirect('dashboard')


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
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    complaints = Complaint.objects.all().order_by('-created_at')
    
    total = complaints.count()
    resolved = complaints.filter(status='Resolved').count()
    
    context = {
        'complaints': complaints[:20],
        'total_complaints': total,
        'pending_count': complaints.filter(status='Pending').count(),
        'in_progress_count': complaints.filter(status='In Progress').count(),
        'resolved_count': resolved,
        'users_count': User.objects.count(),
        'resolution_rate': int((resolved / total * 100) if total > 0 else 0),
    }
    
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='login')
def admin_edit_complaint(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        comment = request.POST.get('comment', '')
        
        if status:
            complaint.status = status
        if priority:
            complaint.priority = priority
        
        complaint.save()
        
        if comment:
            Comment.objects.create(
                complaint=complaint,
                user=request.user,
                text=comment,
                is_staff=True
            )
        
        messages.success(request, 'Complaint updated successfully')
        return redirect('admin_dashboard')
    
    comments = complaint.comments.all()
    context = {'complaint': complaint, 'comments': comments}
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
