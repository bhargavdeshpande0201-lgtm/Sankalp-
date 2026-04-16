# SANKALP - Frontend Documentation

## 📁 Frontend Structure

### Templates Created

```
sankalp/core/templates/
├── base.html                 # Main layout with navigation
├── index.html               # Home/Landing page
├── login.html               # User login page
├── register.html            # User registration page
├── dashboard.html           # User dashboard (main page)
├── add_complaint.html       # Complaint submission form
├── complaint_detail.html    # Individual complaint view
└── admin_dashboard.html     # Admin control panel
```

### Static Files

```
sankalp/core/static/
├── css/
│   └── style.css           # Custom styling
└── js/
    └── script.js           # JavaScript functionality
```

---

## 🎨 Page Descriptions

### 1. **base.html** - Main Template
- Responsive navigation bar with Bootstrap
- User authentication indicators
- Message display system
- Footer
- All pages extend from this template

**Features:**
- Navigation with role-based menu
- User profile dropdown
- Admin access indicator
- Logout functionality

---

### 2. **index.html** - Home Page
- Hero section with project introduction
- Feature cards (Easy Reporting, Real-time Tracking, Secure & Safe)
- Campus statistics display
- Call-to-action sections

**Sections:**
- Welcome banner
- Why SANKALP? (3 feature cards)
- Campus statistics (Total, Pending, In Progress, Resolved)
- CTA for reporting issues

---

### 3. **login.html** - Login Page
- Clean, centered login form
- Username/Email field
- Password field
- Remember me checkbox
- Login button
- Link to registration
- Demo credentials section

**Features:**
- Email validation
- Form validation
- Professional card design
- Demo credentials for testing

---

### 4. **register.html** - Registration Page
- User registration form
- Username field
- Email field
- User role selection (Student/Staff/Admin)
- Password strength requirements
- Password confirmation
- Terms & Conditions checkbox

**Features:**
- Password strength validation
- Role-based registration
- Email validation
- Terms acceptance required

---

### 5. **dashboard.html** - User Dashboard
- Welcome message with user name
- Quick statistics (Total, Pending, In Progress, Resolved)
- Complaint list table with status indicators
- Quick links sidebar
- Issue categories reference
- Report new issue button

**Sections:**
- Statistics cards (4 cards showing complaint counts)
- Complaint table (sortable, filterable)
- Quick actions sidebar
- Categories reference info

---

### 6. **add_complaint.html** - Report Issue Form
- Issue title input
- Category selection dropdown
- Detailed description field
- Location input
- Image upload with drag-and-drop
- Priority level selection
- Anonymous reporting option
- Tips for effective reporting

**Features:**
- Drag-and-drop image upload
- Image preview
- Form validation
- Multiple file format support
- Priority levels (Low, Medium, High)

---

### 7. **complaint_detail.html** - Complaint View
- Full complaint details
- Status badge
- Complainant information
- Date/location information
- Attached image display
- Status update form (for staff/admin)
- Comments section
- Status timeline
- Quick actions

**Sections:**
- Complaint header with ID and category
- Detailed information grid
- Status update form
- Comments timeline
- Supporting actions

---

### 8. **admin_dashboard.html** - Admin Control Panel
- Dashboard statistics (4 cards)
- All complaints table with filter buttons
- Filter by status
- Category breakdown
- Staff assignment form
- Recent activity timeline

**Sections:**
- Statistics overview
- Complaints management table
- Status filters
- Category breakdown
- Staff assignment
- Activity timeline

---

## 🎯 Key Features

### Responsive Design
- Mobile-first approach
- Works on all devices (desktop, tablet, mobile)
- Bootstrap grid system
- Flexible layouts

### User Authentication
- Login/Register system
- Role-based access control
- Session management
- User profile dropdown

### Form Handling
- Client-side validation
- Server-side validation ready
- Error messages
- Success notifications

### Data Display
- Tables with hover effects
- Status badges with color coding
- Icons for visual clarity
- Filter and search functionality

### User Experience
- Toast notifications
- Confirmation dialogs
- Loading states
- Smooth transitions
- Intuitive navigation

---

## 🛠️ Technologies Used

### Frontend Framework
- **Bootstrap 5.3** - Responsive UI components
- **Font Awesome 6.4** - Icons
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript (Vanilla)** - Interactivity

### Color Scheme
- Primary: #667eea (Purple-blue)
- Secondary: #764ba2 (Deep purple)
- Success: #10b981 (Green)
- Warning: #f59e0b (Amber)
- Danger: #ef4444 (Red)
- Info: #3b82f6 (Blue)

---

## 📋 CSS Custom Variables

```css
--primary: #667eea
--primary-dark: #5568d3
--secondary: #764ba2
--success: #10b981
--warning: #f59e0b
--danger: #ef4444
--info: #3b82f6
--light: #f3f4f6
--dark: #1f2937
--muted: #6b7280
```

---

## ✨ JavaScript Utilities

### Available Functions

1. **Form Validation**
   - `setupFormValidation()` - Initialize form validation
   - `validateEmail(email)` - Validate email format
   - `validatePasswordStrength(password)` - Check password strength

2. **Notifications**
   - `showToast(message, type)` - Display toast notification

3. **Search & Filter**
   - `setupSearch()` - Initialize search functionality
   - `setupFilters()` - Initialize filter buttons

4. **Data Management**
   - `exportTableToCSV(tableId, filename)` - Export table to CSV
   - `sortTable(columnIndex)` - Sort table columns

5. **Storage**
   - `StorageUtil.set(key, value)` - Save to localStorage
   - `StorageUtil.get(key)` - Retrieve from localStorage
   - `StorageUtil.remove(key)` - Delete from localStorage
   - `StorageUtil.clear()` - Clear all localStorage

6. **Utilities**
   - `formatDate(date)` - Format date display
   - `formatDateTime(date)` - Format date and time
   - `debounce(func, delay)` - Debounce function calls
   - `throttle(func, limit)` - Throttle function calls

---

## 🚀 How to Use

### 1. Setup Django Configuration
Add to `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'core',
]

STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static',
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### 2. Create Views

```python
# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {
        'complaints': complaints,
        'total_complaints': complaints.count(),
        'pending_count': complaints.filter(status='Pending').count(),
        'in_progress_count': complaints.filter(status='In Progress').count(),
        'resolved_count': complaints.filter(status='Resolved').count(),
    })
```

### 3. Setup URLs

```python
# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
]
```

---

## 📱 Responsive Breakpoints

- **xs**: < 576px (Mobile)
- **sm**: ≥ 576px (Small tablet)
- **md**: ≥ 768px (Tablet)
- **lg**: ≥ 992px (Desktop)
- **xl**: ≥ 1200px (Large desktop)

---

## 🎓 For Viva/Presentation

### Key Points to Explain
1. **Three-tier architecture:** Frontend handles UI, Backend handles logic, Database stores data
2. **User roles:** Student, Staff, Admin - each with different permissions
3. **Responsive design:** Works on all devices
4. **User experience:** Easy to use, intuitive interface
5. **Data validation:** Client-side and server-side validation
6. **Security:** Role-based access control

### Screenshots to Prepare
- Home page
- Login/Register pages
- Student dashboard
- Complaint submission
- Admin dashboard
- Complaint detail view

---

## ✅ Checklist for Next Steps

- [ ] Setup Django models
- [ ] Create forms using Django forms
- [ ] Connect views to templates
- [ ] Implement authentication
- [ ] Add image upload functionality
- [ ] Test on different browsers
- [ ] Optimize for mobile
- [ ] Add error handling
- [ ] Implement pagination
- [ ] Add search functionality

---

## 📄 Notes

- All templates use Bootstrap 5.3 for responsive design
- Custom CSS adds professional styling on top of Bootstrap
- JavaScript is modular and easy to extend
- Forms include validation messages
- Icons are from Font Awesome 6.4
- Color scheme matches a professional campus management system theme

---

**Frontend Ready for Backend Integration! 🚀**
