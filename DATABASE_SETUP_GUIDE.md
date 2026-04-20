# 🗄️ SANKALP Database Setup - Complete Step-by-Step Guide

This guide explains how the database works and how to set it up properly.

---

## 📋 Table of Contents
1. [Database Overview](#database-overview)
2. [Step-by-Step Setup](#step-by-step-setup)
3. [Database Structure](#database-structure)
4. [Common Issues & Fixes](#common-issues--fixes)
5. [Testing the Database](#testing-the-database)
6. [Admin Features](#admin-features)

---

## 🗂️ Database Overview

### What is a Database?
A database stores all your application data (users, complaints, comments) in an organized way.

### SANKALP Uses:
- **SQLite** (Simple, file-based database)
- **Location**: `sankalp/db.sqlite3`
- **Perfect for**: Development and small deployments

### Database Tables in SANKALP:

**1. Users (from Django)**
```
- id: Unique ID
- username: Username
- email: Email address
- password: Hashed password
- is_staff: Is this user a staff/admin?
- is_superuser: Is this user a superuser/admin?
```

**2. Complaints (Custom)**
```
- id: Unique complaint ID
- user_id: Which user filed this complaint
- title: Complaint title
- description: Detailed description
- category: Category (Waste, Parking, Infrastructure, Security)
- status: Status (Pending, In Progress, Resolved, Rejected)
- priority: Priority (low, medium, high)
- location: Location of issue
- image: Uploaded image file
- anonymous: Is complaint anonymous?
- created_at: When was it created
- updated_at: When was it last updated
```

**3. Comments (Custom)**
```
- id: Unique comment ID
- complaint_id: Which complaint this comment is for
- user_id: Who wrote this comment
- text: Comment text
- is_staff: Is this a staff comment?
- created_at: When was it created
```

---

## 🚀 Step-by-Step Setup

### Step 1: Open Terminal/PowerShell
**On Windows:**
- Press `Windows Key + R`
- Type `powershell`
- Press Enter

### Step 2: Navigate to Project Directory
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\Sankalp Campus management system"
```

### Step 3: Create Virtual Environment (if not exists)
```powershell
python -m venv venv
```

### Step 4: Activate Virtual Environment
```powershell
venv\Scripts\activate
```
*(You should see `(venv)` appear on the left of the terminal)*

### Step 5: Install Required Packages
```powershell
pip install -r requirements.txt
```

### Step 6: Navigate to Django Project
```powershell
cd sankalp
```

### Step 7: Create Migrations (if not already done)
This tells Django what database tables to create based on your models.
```powershell
python manage.py makemigrations
```

### Step 8: Apply Migrations
This actually creates the tables in the database.
```powershell
python manage.py migrate
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying ... OK
  Applying ... OK
  ...
```

### Step 9: Create a Superuser (Admin Account)
```powershell
python manage.py createsuperuser
```

**Follow the prompts:**
```
Username: admin
Email: admin@sankalp.com
Password: (choose a strong password)
Password (again): (repeat password)
Superuser created successfully.
```

### Step 10: Run the Development Server
```powershell
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
```

### Step 11: Access the Application
Open your browser and go to:
- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🏗️ Database Structure

### Model Relationships

```
┌─────────────┐
│ Django User │
└──────┬──────┘
       │
       │ (One User has Many Complaints)
       │
       ▼
┌──────────────┐      ┌──────────────┐
│  Complaint   │ ◄────┤  Comments    │
│              │      │              │
│ - user_id    │      │ - complaint  │
│ - title      │      │ - user       │
│ - category   │      │ - text       │
│ - status     │      └──────────────┘
│ - priority   │
│ - location   │
│ - image      │
└──────────────┘
```

### Relationships Explained:

**1. User → Complaint (One-to-Many)**
- One user can file many complaints
- Each complaint belongs to exactly one user
- If user is deleted, all their complaints are deleted (CASCADE)

**2. Complaint → Comment (One-to-Many)**
- One complaint can have many comments
- Each comment belongs to exactly one complaint
- If complaint is deleted, all comments are deleted (CASCADE)

**3. User → Comment (One-to-Many)**
- One user can write many comments
- Each comment is written by one user
- If user is deleted, all comments are deleted (CASCADE)

---

## 🔄 Common Operations

### Add a New Complaint
```
1. User logs in
2. Clicks "Add Complaint"
3. Fills form with title, description, etc.
4. Database INSERT: New row added to Complaints table
5. Status automatically set to "Pending"
6. Timestamp automatically recorded
```

### Update Complaint Status (Admin)
```
1. Admin logs in with staff account
2. Goes to admin dashboard
3. Clicks edit on a complaint
4. Changes status to "In Progress", "Resolved", etc.
5. Database UPDATE: Status field updated
6. Timestamp automatically recorded
```

### Delete a Complaint
```
1. User or Admin can delete
2. Database DELETE: Removed from Complaints table
3. All related comments are also deleted (CASCADE)
4. User is redirected to dashboard
```

### Add Comment
```
1. User posts comment on complaint
2. Database INSERT: New row in Comments table
3. Links to both complaint and user
4. Staff flag indicates if it's admin comment
```

---

## ❌ Common Issues & Fixes

### Issue 1: "No such table: core_complaint"
**Cause**: Migrations haven't been applied

**Fix**:
```powershell
python manage.py migrate
```

### Issue 2: "Database is locked"
**Cause**: Multiple processes accessing database

**Fix**:
```powershell
# Stop the server (Ctrl+C)
# Wait 5 seconds
# Run again: python manage.py runserver
```

### Issue 3: Can't login to admin panel
**Cause**: Superuser not created or wrong credentials

**Fix**:
```powershell
python manage.py createsuperuser
# Enter new credentials
```

### Issue 4: Image uploads not working
**Cause**: Media folder not configured

**Fix**: Already configured in settings.py
- Images saved to: `sankalp/media/complaints/`
- Check permissions on this folder

### Issue 5: Changes not appearing
**Cause**: Need to restart server

**Fix**:
```powershell
# Press Ctrl+C to stop server
# Wait 2 seconds
# Run: python manage.py runserver
```

---

## ✅ Testing the Database

### Test 1: Check Database Exists
```powershell
# In sankalp directory
ls db.sqlite3
# If file exists, database is created
```

### Test 2: Check Tables Were Created
```powershell
python manage.py dbshell
# Then in SQLite:
# .tables
# (shows all tables)
```

### Test 3: Test User Registration
1. Go to http://127.0.0.1:8000/register
2. Create a student account
3. Check if data appears in admin panel

### Test 4: Test Complaint Submission
1. Login with student account
2. Add a complaint
3. Check admin dashboard to verify complaint appears

### Test 5: Test Complaint Deletion
1. Login with student account
2. Go to your complaint
3. Click delete
4. Verify complaint is removed from dashboard

### Test 6: Test Admin Functions
1. Login with admin/superuser account
2. Go to /admin
3. View complaints, edit status
4. Update a complaint

---

## 👨‍💼 Admin Features

### Admin Panel Features:
- View all complaints from all users
- Filter by category, status, date
- Edit complaint status and priority
- Add staff comments
- View user information

### Admin Dashboard Features:
- Total complaints count
- Pending complaints count
- In-progress complaints count
- Resolved complaints count
- Resolution rate percentage
- User count

### Admin Actions:
- Change complaint status
- Add comments to complaints
- Change priority level
- Delete complaints

### Accessing Admin Panel:
```
URL: http://127.0.0.1:8000/admin/
Username: (superuser username)
Password: (superuser password)
```

---

## 📊 Database Maintenance

### Backup Database
```powershell
# Copy the db.sqlite3 file to a safe location
Copy-Item "db.sqlite3" "db.sqlite3.backup"
```

### Reset Database (Development Only)
```powershell
# Delete the database
Remove-Item "db.sqlite3"

# Reapply migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

### View Database via Admin
1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser account
3. Click on "Complaints" to see all complaints
4. Click on "Comments" to see all comments
5. Click on "Users" to see all users

---

## 🛡️ Security Notes

### Passwords
- All passwords are hashed before storing
- Never stored in plain text
- Cannot be recovered (only reset)

### Permissions
- Regular users can only see their own complaints
- Staff users can see all complaints
- Superuser can do everything

### Database File
- `db.sqlite3` contains all data
- Keep it private
- Never commit to public repositories

---

## 📞 Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `python manage.py makemigrations` | Create migration files |
| `python manage.py migrate` | Apply migrations to database |
| `python manage.py createsuperuser` | Create admin account |
| `python manage.py runserver` | Start development server |
| `python manage.py dbshell` | Open database shell |
| `python manage.py flush` | Clear all data (careful!) |
| `python manage.py collectstatic` | Collect static files |

---

## ✨ You're All Set!

Your database is now ready to use. The system will automatically handle:
- ✅ Creating new complaints
- ✅ Adding comments
- ✅ Deleting complaints and comments
- ✅ Managing user accounts
- ✅ Admin operations
- ✅ Permissions and access control

**Happy complaint managing! 🎉**
