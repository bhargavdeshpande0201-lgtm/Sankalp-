# 🚀 SANKALP - QUICK START GUIDE (Database & Admin Complete)

**Status**: ✅ Database fully configured and tested
**Last Updated**: April 16, 2026
**Ready for**: Development and Testing

---

## ⚡ QUICKEST START (60 seconds)

### Step 1: Open Terminal in Project Folder
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\Sankalp Campus management system"
```

### Step 2: Run the Development Server
```powershell
venv\Scripts\python.exe sankalp/manage.py runserver
```

### Step 3: Open in Browser
```
Home: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/
```

**That's it! 🎉**

---

## 👥 Default Login Credentials

### Admin/Superuser Account
```
URL: http://127.0.0.1:8000/admin/ OR http://127.0.0.1:8000/login (choose Admin)
Username: admin
Password: admin@2024
Role: Superuser (Full access)
```

### Teacher/Staff Account
```
Username: teacher1
Password: Teacher@123
Role: Staff (Can manage complaints)
```

### Student Account
```
Username: student1
Password: Student@123
Role: Student (Can submit/view complaints)
```

**[Create more accounts at http://127.0.0.1:8000/register]**

---

## 📊 Database Overview

### What's Already Set Up ✅

| Component | Status | Details |
|-----------|--------|---------|
| Database File | ✅ Created | `sankalp/db.sqlite3` (159 KB) |
| Database Type | ✅ SQLite3 | Hardcoded in `settings.py` |
| Tables | ✅ Created | Users, Complaints, Comments |
| Migrations | ✅ Applied | All initial migrations done |
| Admin User | ✅ Created | `admin` / `admin@2024` |
| Demo Data | ✅ Loaded | 15 users, 13 complaints, 15 comments |

### Database Statistics
```
📈 Current Numbers:
   • Total Users: 15
   • Total Complaints: 13
   • Total Comments: 15
   
👥 User Distribution:
   • Admins: 1
   • Staff/Teachers: 5
   • Students: 9
```

---

## 🔧 Database Operations

### 1. View All Complaints
```python
# In Django Shell
from core.models import Complaint
Complaint.objects.all()
```

### 2. View User Complaints
```python
from core.models import Complaint
from django.contrib.auth.models import User

user = User.objects.get(username='student1')
user.complaints.all()
```

### 3. Filter by Status
```python
Complaint.objects.filter(status='Pending')
Complaint.objects.filter(status='In Progress')
Complaint.objects.filter(status='Resolved')
```

### 4. Count Complaints
```python
Complaint.objects.count()
Complaint.objects.filter(status='Pending').count()
```

### 5. Add Comment to Complaint
```python
from core.models import Comment, Complaint

complaint = Complaint.objects.get(id=1)
Comment.objects.create(
    complaint=complaint,
    user=user,
    text="This has been resolved",
    is_staff=True
)
```

---

## 🎯 Key Features Implemented

### ✅ Student Features
- Create complaints
- View own complaints
- Add comments
- Update profile
- Delete own complaints (except resolved ones)
- Search complaints

### ✅ Admin/Staff Features
- View all complaints
- Filter by status/category/priority
- Update complaint status
- Add staff comments
- Paginated dashboard (15 per page)
- View statistics and metrics
- Edit priorities
- User management

### ✅ Admin Dashboard Features
- **Total Complaints Counter**: Shows all complaints
- **Pending Count**: Not yet processed
- **In Progress Count**: Being worked on
- **Resolved Count**: Completed
- **Rejected Count**: Not allowed
- **High Priority Count**: Urgent issues
- **Resolution Rate**: % of resolved complaints
- **User Count**: Total registered users
- **Category Breakdown**: Stats by category
- **Pagination**: 15 complaints per page
- **Filters**: Status, Category, Priority

---

## 🔐 Admin Login & Dashboard Features

### Admin Login (Role-Based)
1. Go to http://127.0.0.1:8000/login
2. Choose role as "Admin" 
3. Enter credentials (admin / admin@2024)

### Admin Dashboard (http://127.0.0.1:8000/admin-dashboard)
Features:
- 📊 View complaint statistics at a glance
- 🔍 Filter complaints by status, category, priority
- 📄 Paginated complaint lists (15 per page)
- ✏️ Edit any complaint
- 💬 Add staff comments
- 📈 See resolution rate percentage

### How to Use Admin Dashboard

#### View All Complaints
1. Login with admin account
2. Go to Admin Dashboard
3. See all complaints with their status

#### Filter Complaints
- By Status: Choose Pending/In Progress/Resolved/Rejected
- By Category: Choose Waste/Parking/Infrastructure/Security
- By Priority: Choose Low/Medium/High

#### Edit a Complaint
1. Click on any complaint
2. Click "Edit" or change status dropdown
3. Add staff comment if needed
4. Save changes

#### Change Status
1. Select complaint
2. Choose new status from dropdown
3. Add comment explaining the change
4. Status updates with timestamp

---

## 💾 Delete Complaint Function

### How Delete Works
- **Your own complaint**: Can delete unless it's Resolved or Rejected
- **As Admin**: Can delete any complaint
- **Cascade Delete**: All comments are also deleted
- **Permission Check**: Unauthorized deletions blocked with error

### When You CAN'T Delete
- ❌ Resolved complaints (as regular user)
- ❌ Rejected complaints (as regular user)
- ❌ Someone else's complaint (as regular user)
- ✅ You CAN delete if you're the admin

---

## 🧪 Database Testing

### Run Test Suite
```powershell
cd sankalp
..\venv\Scripts\python.exe test_database.py
```

### What Gets Tested
1. Database Connection
2. All Tables Exist
3. User Authentication
4. User Roles Distributed
5. Complaint Model
6. Comment Model
7. Model Relationships
8. Choice Fields
9. ORM Operations
10. Data Integrity
11. Performance

**Result**: ✅ All tests passed!

---

## 🛠️ Useful Django Commands

### Database Operations
```powershell
cd sankalp

# Show migrations
python manage.py showmigrations

# Make new migrations (if you change models)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (careful!)
python manage.py flush
```

### User Management
```powershell
# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Run setup script
python setup_database.py
```

### Server Operations
```powershell
# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8001

# Run tests
python manage.py test
```

---

## 📁 Important Files

### Core Files
- `sankalp/db.sqlite3` - Database file
- `sankalp/core/models.py` - Data models
- `sankalp/core/views.py` - Business logic
- `sankalp/core/forms.py` - Form definitions
- `sankalp/settings.py` - Configuration

### Database Files
- `DATABASE_SETUP_GUIDE.md` - Detailed setup (this one!)
- `sankalp/setup_database.py` - Setup script
- `sankalp/test_database.py` - Test script

---

## 🚨 Troubleshooting

### "Cannot find database file"
**Solution**: Make sure you're in the `sankalp` directory:
```powershell
cd sankalp
python manage.py migrate
```

### "ModuleNotFoundError: No module named 'django'"
**Solution**: Install dependencies:
```powershell
pip install -r requirements.txt
```

### "Port 8000 already in use"
**Solution**: Use a different port:
```powershell
python manage.py runserver 8001
```

### "Permission denied" on delete
**Solution**: Check permission roles in admin panel

### "No such table: core_complaint"
**Solution**: Run migrations:
```powershell
python manage.py migrate
```

---

## ✨ What's Working Now

### ✅ Database Layer
- SQLite database created and synced
- All tables created with migrations
- Foreign keys and relationships working
- Data integrity validated

### ✅ User Authentication
- Register new users
- Login with roles (Student/Staff/Admin)
- Logout functionality
- Session management

### ✅ Complaint Management
- Create complaints (students)
- View own complaints (students)
- View all complaints (admin)
- Update status (admin)
- Delete complaints (with permissions)
- Add comments
- Filter & search

### ✅ Admin Features
- Admin dashboard with statistics
- Filter complaints by status/category/priority
- Edit complaint details
- Add staff comments
- View user management
- Pagination of results

---

## 🎯 Next Steps (Optional)

### If You Want to Extend
1. **Add new fields to complaints**:
   - Edit `models.py`
   - Run `python manage.py makemigrations`
   - Run `python manage.py migrate`

2. **Add email notifications**:
   - Install `django-mail`
   - Add email backend in `settings.py`

3. **Add export to PDF**:
   - Install `reportlab`
   - Add export view

4. **Improve UI**:
   - Update HTML templates
   - Enhance CSS styling

---

## 📞 Quick Reference

### Credentials
```
Admin: admin / admin@2024
Teacher: teacher1 / Teacher@123
Student: student1 / Student@123
```

### URLs
```
Home:      http://127.0.0.1:8000/
Admin:     http://127.0.0.1:8000/admin/
Login:     http://127.0.0.1:8000/login
Register:  http://127.0.0.1:8000/register
Dashboard: http://127.0.0.1:8000/dashboard
Complaints: http://127.0.0.1:8000/add-complaint
```

### Commands
```powershell
# Start server
python manage.py runserver

# Run tests
python test_database.py

# Setup database
python setup_database.py

# Access shell
python manage.py shell
```

---

## 🎉 You're All Set!

Your SANKALP Campus Management System is:
- ✅ Database fully set up
- ✅ Admin authenticated
- ✅ All features tested
- ✅ Ready for use!

**Start the server and enjoy!**

```powershell
python manage.py runserver
```

Then visit: http://127.0.0.1:8000/

---

**Questions?** Check DATABASE_SETUP_GUIDE.md for detailed information.
