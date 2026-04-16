# SANKALP Campus Management System - Complete Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (optional)

### Installation Steps

#### 1. Clone/Download the Project
```bash
cd your-projects-folder
# If using git:
git clone <repository-url>
# Or manually extract the project folder
```

#### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Navigate to Project Directory
```bash
cd sankalp
```

#### 5. Apply Migrations
```bash
python manage.py migrate
```

#### 6. Create Superuser (Optional - for Django Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

#### 7. Run Development Server
```bash
python manage.py runserver
# Server will run at http://127.0.0.1:8000/
```

#### 8. Access the Application
- **Home Page**: http://127.0.0.1:8000/
- **Django Admin**: http://127.0.0.1:8000/admin/

---

## 📝 Default Demo Accounts

### Student Account
```
Username: student1
Password: password123
```

### Teacher/Staff Account
```
Username: teacher1
Password: password123
```

### Admin Account
```
Username: admin
Password: admin123
```

---

## 🔒 Security Notes

⚠️ **Important for Production:**
1. Change the `SECRET_KEY` in `sankalp/settings.py`
2. Set `DEBUG = False` in production
3. Update `ALLOWED_HOSTS` with your domain
4. Use environment variables for sensitive data
5. Use a production-grade database (PostgreSQL recommended)
6. Configure proper CORS settings

---

## 📂 Project Structure

```
sankalp/
├── manage.py                    # Django management script
├── db.sqlite3                   # Database file
├── sankalp/                     # Project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
└── core/                        # Main application
    ├── models.py                # Database models
    ├── views.py                 # View logic (15+ views)
    ├── urls.py                  # App URL routing
    ├── admin.py                 # Django admin configuration
    ├── forms.py                 # Django forms
    ├── migrations/              # Database migrations
    ├── static/                  # Static files
    │   ├── css/style.css        # Custom styling (650+ lines)
    │   └── js/script.js         # JavaScript utilities (400+ lines)
    └── templates/               # HTML templates (11 files)
        ├── base.html            # Master template
        ├── index.html           # Home page
        ├── login.html           # Login page
        ├── register.html        # Registration page
        ├── dashboard.html       # Student dashboard
        ├── add_complaint.html    # Complaint form
        ├── complaint_detail.html # Complaint details
        ├── admin_dashboard.html  # Admin panel
        ├── admin_edit_complaint.html  # Admin editor
        ├── profile.html         # User profile
        └── search_complaints.html       # Search page
```

---

## 🎯 Features

### 1. **Authentication**
- Role-based login (Student, Teacher/Staff, Admin)
- Secure password hashing
- Session management
- Profile management

### 2. **Complaint Management**
- Submit complaints with title, category, description, location, and images
- Track complaint status in real-time
- Add comments to complaints
- View complaint history
- Search and filter complaints

### 3. **User Roles**
- **Student**: Submit and track complaints
- **Teacher/Staff**: Manage and respond to complaints
- **Admin**: System administration and analytics

### 4. **Dashboard**
- Student dashboard with complaint statistics
- Admin dashboard with analytics and controls
- Real-time status updates

### 5. **Additional Features**
- Anonymous complaint submission option
- Priority levels (Low, Medium, High)
- Category-based organization
- Complaint comments and updates
- User profile management
- Password change functionality

---

## 🔧 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Home page |
| GET/POST | `/register` | User registration |
| GET/POST | `/login` | User login |
| GET | `/logout` | User logout |
| GET | `/dashboard` | Student dashboard |
| GET/POST | `/add-complaint` | Create complaint |
| GET | `/complaint/<id>` | View complaint details |
| POST | `/complaint/<id>/comment` | Add comment |
| POST | `/complaint/<id>/delete` | Delete complaint |
| POST | `/complaint/<id>/update-status` | Update status |
| GET | `/search` | Search complaints |
| GET | `/profile` | User profile |
| POST | `/profile/update` | Update profile |
| POST | `/profile/change-password` | Change password |
| GET | `/admin-dashboard` | Admin panel |
| GET/POST | `/admin/complaint/<id>` | Admin edit complaint |

---

## 📊 Database Models

### User Model (Django Built-in)
- username, email, password (hashed)
- first_name, last_name
- is_staff (for teachers)
- is_superuser (for admins)

### Complaint Model
- id, user (ForeignKey)
- title, description, category, status, priority
- location, image, anonymous flag
- created_at, updated_at timestamps

### Comment Model
- id, complaint (ForeignKey), user (ForeignKey)
- text content, is_staff flag
- created_at timestamp

---

## 🐛 Troubleshooting

### Database Errors
```bash
# Reset database
python manage.py migrate --run-syncdb
```

### Missing Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Port Already in Use
```bash
# Run on different port
python manage.py runserver 0.0.0.0:8001
```

### Template Not Found
- Ensure `TEMPLATE_DIRS` in settings.py is configured correctly
- Check template file names match URL names

---

## 📧 Support & Contact

For issues or questions:
1. Check the troubleshooting section above
2. Review Django documentation: https://docs.djangoproject.com/
3. Check application logs for detailed error messages

---

## 📄 License

SANKALP Campus Management System - Educational Project
Created for: Zeal Institute of Business Administration, Computer Application & Research

---

## ✨ Contributors

- Project Team
- Zeal Institute

---

**Last Updated**: April 11, 2026  
**Version**: 1.0.0 - Complete Edition
