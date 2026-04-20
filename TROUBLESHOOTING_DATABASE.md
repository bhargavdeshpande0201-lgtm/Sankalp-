# 🔧 SANKALP DATABASE & ADMIN - TROUBLESHOOTING GUIDE

**Last Updated**: April 16, 2026
**Status**: All systems operational ✅

---

## 🚨 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'django'"

**Symptoms**: 
- Can't start server
- ImportError when running scripts

**Diagnosis**:
```powershell
# Check if Django is installed
python -m pip list | findstr Django
```

**Solutions**:

**Option A: Install dependencies**
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\Sankalp Campus management system"
pip install -r requirements.txt
```

**Option B: Use virtual environment**
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\Sankalp Campus management system"
venv\Scripts\python.exe -m pip install django pillow python-decouple
```

**Option C: Explicitly install**
```powershell
pip install Django==6.0.3 Pillow==12.2.0 python-decouple==3.8
```

---

### Issue 2: "No such table: core_complaint"

**Symptoms**:
- Database error when accessing complaints
- 500 Internal Server Error
- "ProgrammingError" in terminal

**Diagnosis**:
```powershell
# Check if migrations are applied
python manage.py showmigrations core
```

**Solutions**:

**Option A: Apply all migrations**
```powershell
cd sankalp
python manage.py migrate
```

**Option B: Reset and reconnect database**
```powershell
# Backup first!
Copy-Item db.sqlite3 db.sqlite3.backup
# Reset
python manage.py migrate
```

**Option C: Create fresh database**
```powershell
# Backup old database
Copy-Item db.sqlite3 db.sqlite3.old
# Create new migrations
python manage.py makemigrations
# Apply migrations
python manage.py migrate
# Create superuser
python manage.py createsuperuser
```

---

### Issue 3: "Database is locked"

**Symptoms**:
- "database is locked" error
- Can't write to database
- Timeout errors

**Diagnosis**:
Check if multiple processes are accessing database

**Solutions**:

**Option A: Restart server**
```powershell
# Stop server (Ctrl+C in terminal)
# Wait 3 seconds
# Restart: python manage.py runserver
```

**Option B: Close all Python processes**
```powershell
# In PowerShell:
Get-Process python | Stop-Process
# Wait 2 seconds, restart server
```

**Option C: Check file permissions**
```powershell
# Make database writable
Get-Item db.sqlite3
# If issue persists, copy to temp location:
Copy-Item db.sqlite3 C:\Temp\
```

---

### Issue 4: "Port 8000 already in use"

**Symptoms**:
- "Port 8000 already in use! Trying port 8001..."
- Previous server still running

**Diagnosis**:
Check which process is using port 8000

**Solutions**:

**Option A: Use different port**
```powershell
python manage.py runserver 8001
# Then access: http://127.0.0.1:8001/
```

**Option B: Kill process on port**
```powershell
# Find process
netstat -ano | findstr :8000
# Kill it (replace PID with actual number)
taskkill /PID 1234 /F
# Then restart
python manage.py runserver
```

**Option C: Force port with bind**
```powershell
python manage.py runserver 127.0.0.1:9000
```

---

### Issue 5: "CSRF verification failed"

**Symptoms**:
- 403 Forbidden error
- "CSRF token missing or incorrect"
- Form submission fails

**Diagnosis**:
CSRF token not in form

**Solutions**:

**Option A: Check form includes CSRF**
All forms should have:
```html
{% csrf_token %}
```

**Option B: Check CSRF middleware**
In `settings.py`, ensure:
```python
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]
```

**Option C: Clear browser cache**
- Clear cookies for 127.0.0.1:8000
- Close and reopen browser
- Try again

---

### Issue 6: "Cannot find file 'db.sqlite3'"

**Symptoms**:
- Database file missing
- "FileNotFoundError" 
- Migration shows no tables

**Diagnosis**:
Check if you're in correct directory

**Solutions**:

**Option A: Verify location**
```powershell
# Should be in sankalp directory
ls db.sqlite3
# If not found, you're in wrong directory
cd sankalp
ls db.sqlite3
```

**Option B: Check settings.py**
```powershell
# Open settings.py and verify:
# DATABASE['NAME'] = BASE_DIR / 'db.sqlite3'
```

**Option C: Create new database**
```powershell
# Navigate to sankalp folder
cd sankalp
# Create new database
python manage.py migrate
```

---

### Issue 7: "Admin login not working"

**Symptoms**:
- "Invalid credentials for Admin login"
- Can login as student but not admin
- Admin page gives permission error

**Diagnosis**:
Wrong credentials or user permissions

**Solutions**:

**Option A: Verify admin credentials**
```powershell
# Check admin exists
python manage.py shell
# In shell:
from django.contrib.auth.models import User
User.objects.get(username='admin')
```

**Option B: Create new superuser**
```powershell
python manage.py createsuperuser
# Follow prompts
```

**Option C: Check permissions**
```powershell
# Run in Django shell
from django.contrib.auth.models import User
admin = User.objects.get(username='admin')
print(admin.is_superuser)
print(admin.is_staff)
# Both should be True
```

**Option D: Reset admin password**
```powershell
python manage.py changepassword admin
# Enter new password
```

---

### Issue 8: "Delete complaint not working"

**Symptoms**:
- "You do not have permission" error
- Delete button hidden
- Confirmation doesn't work

**Diagnosis**:
Permission or condition not met

**Solutions**:

**Option A: Check complaint status**
- Can only delete: Pending, In Progress
- Cannot delete: Resolved, Rejected (as student)
- Admins can always delete

**Option B: Verify you're the owner**
- Only complaint creator can delete (unless admin)
- Admin can delete any complaint

**Option C: Check delete in database**
```powershell
python manage.py shell
from core.models import Complaint
complaint = Complaint.objects.get(id=1)
print(complaint.user.username)  # Should be your username
# Delete directly:
complaint.delete()
```

---

### Issue 9: "Admin Dashboard showing blank/errors"

**Symptoms**:
- Admin dashboard page doesn't load
- 500 error instead of dashboard
- Statistics not showing

**Diagnosis**:
View has bugs or permissions issue

**Solutions**:

**Option A: Check permissions**
- Make sure logged-in user is staff/admin
- Check terminal for error messages
- Verify is_staff or is_superuser is True

**Option B: Check database**
```powershell
python manage.py shell
from core.models import Complaint
Complaint.objects.count()
# Should return a number
```

**Option C: Clear cache**
```powershell
# Stop server (Ctrl+C)
# Wait 3 seconds
# Delete .pyc files (if found):
Remove-Item -Recurse ./__pycache__
# Restart server
python manage.py runserver
```

---

### Issue 10: "Comments not saving"

**Symptoms**:
- Comment added but doesn't appear
- No error message
- Page reloads but comment missing

**Diagnosis**:
Comment not being saved to database

**Solutions**:

**Option A: Check complaint exists**
```powershell
# Make sure complaint ID is valid
python manage.py shell
from core.models import Complaint
Complaint.objects.filter(id=1).exists()
```

**Option B: Check permissions**
- Only owner or staff can comment
- Try with staff account

**Option C: Debug add_comment view**
- Check form POST data
- Verify text field not empty
- Check user is authenticated

---

### Issue 11: "Static files not loading (CSS/Images)"

**Symptoms**:
- Page loads but looks plain (no styling)
- Images not showing
- CSS not applied

**Diagnosis**:
Static files not served properly

**Solutions**:

**Option A: Check STATIC_URL setting**
```powershell
# In settings.py, should have:
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**Option B: Collect static files (production)**
```powershell
python manage.py collectstatic --noinput
```

**Option C: Check file exists**
```powershell
# CSS should be at:
# sankalp/core/static/css/style.css
ls core/static/css/style.css
```

**Option D: Verify dev server serving static**
Django dev server auto-serves static files
- Restart server if changed
- Check console for 404 errors

---

### Issue 12: "Image upload not working"

**Symptoms**:
- Upload button exists but doesn't save image
- File appears selected but not saved
- No image file in media folder

**Diagnosis**:
Media files directory issue

**Solutions**:

**Option A: Check media folder exists**
```powershell
# Should exist at: sankalp/media/complaints/
# Create if missing:
New-Item -ItemType Directory -Path media/complaints -Force
```

**Option B: Check permissions**
- Folder should be writable
- Check Windows permissions

**Option C: Verify settings**
```python
# settings.py should have:
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Option D: Test upload**
```powershell
# Create test image
# Try uploading through web interface
# Check media/complaints/ folder
```

---

### Issue 13: "500 Internal Server Error"

**Symptoms**:
- "500 Internal Server Error" page
- No specific error message
- Server error in terminal

**Diagnosis**:
Check terminal output

**Solutions**:

**Option A: Check terminal for error**
- Terminal should show full error
- Stack trace shows which file has issue
- Copy error and search online

**Option B: Enable debug logging**
```python
# In views.py, add logging
import logging
logger = logging.getLogger(__name__)
logger.error("Your message")
```

**Option C: Check database integrity**
```powershell
python test_database.py
# Should show if database corrupted
```

**Option D: Check recent changes**
- Revert recent code changes
- Check syntax errors
- Look for missing imports

---

### Issue 14: "Permission denied accessing admin"

**Symptoms**:
- "Access denied. Admin privileges required"
- Admin dashboard redirects to login
- Can't access /admin/ URL

**Diagnosis**:
Not logged in as admin/staff

**Solutions**:

**Option A: Login with admin account**
- Go to /login
- Select "Admin" role
- Use: admin / admin@2024

**Option B: Check user permissions**
```powershell
python manage.py shell
from django.contrib.auth.models import User
user = User.objects.get(username='student1')
print(user.is_staff)  # Should be False
# To make user staff:
user.is_staff = True
user.save()
```

**Option C: Access Django admin instead**
- Go to http://127.0.0.1:8000/admin/
- Login with admin credentials
- From there you can manage users

---

### Issue 15: "Complaint not appearing in admin dashboard"

**Symptoms**:
- Created complaint but admin can't see it
- Filter returns 0 results
- Complaint deleted unexpectedly

**Diagnosis**:
Complaint not saved correctly

**Solutions**:

**Option A: Check database directly**
```powershell
python manage.py shell
from core.models import Complaint
Complaint.objects.count()  # Check if exists
complaint = Complaint.objects.filter(title='Your Title')
```

**Option B: Check complaint permissions**
- Only owner sees own complaints in student view
- Admin can see all complaints

**Option C: Refresh page**
- Reload with Ctrl+Shift+Delete (hard refresh)
- Close and reopen browser
- Restart server

---

## 🆘 Emergency Fixes

### If Nothing Works

**Option 1: Reset Database (Development Only)**
```powershell
cd sankalp

# Backup current database
Copy-Item db.sqlite3 db.sqlite3.backup

# Delete current database
Remove-Item db.sqlite3

# Recreate
python manage.py migrate

# Create new admin
python manage.py createsuperuser

# Run setup
python setup_database.py
```

**Option 2: Reinstall Python packages**
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\Sankalp Campus management system"

# Deactivate venv
deactivate

# Remove venv
Remove-Item -Recurse venv

# Create new venv
python -m venv venv

# Activate
venv\Scripts\Activate.ps1

# Install
pip install -r requirements.txt
```

**Option 3: Console Log for debugging**
```powershell
# Run server with verbose output
python manage.py runserver --verbosity 3

# Check database logs
python manage.py dbshell
# Then: SELECT * FROM sqlite_master;
```

---

## ✅ Health Checks

### Quick Tests to Verify Everything Works

```powershell
# Test 1: Database connectivity
python test_database.py

# Test 2: Run migrations
python manage.py migrate

# Test 3: Check admin exists
python manage.py shell
# Type: from django.contrib.auth.models import User; User.objects.get(username='admin')

# Test 4: Start server
python manage.py runserver

# Test 5: Access home page
# Visit http://127.0.0.1:8000/ in browser

# Test 6: Login
# Try login with: admin / admin@2024

# Test 7: Create complaint
# Create test complaint as student

# Test 8: Delete complaint
# Delete test complaint as student or admin

# Test 9: Admin dashboard
# Go to /admin-dashboard as admin
```

---

## 📞 Support Commands

### Useful Debug Commands

```powershell
# Show all users
python manage.py shell
# from django.contrib.auth.models import User
# for u in User.objects.all(): print(u.username, u.is_staff)

# Show all complaints
# from core.models import Complaint
# Complaint.objects.all()

# Show database info
python manage.py dbshell
# .tables
# .quit

# Check for errors
python manage.py check

# Show migrations
python manage.py showmigrations

# See what changed
python manage.py sqlmigrate core 0001

# Run specific tests
python manage.py test core

# Create backup
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json
```

---

## 📊 Performance Issues

### If Page is Slow

**Option 1: Add database indexing**
```python
# In models.py add Meta class:
class Meta:
    indexes = [
        models.Index(fields=['status']),
        models.Index(fields=['user']),
    ]
```

**Option 2: Use pagination**
Already implemented in admin dashboard - 15 per page

**Option 3: Optimize queries**
```python
# Use select_related for foreign keys
Complaint.objects.select_related('user')

# Use only() to get specific fields
Complaint.objects.only('id', 'title', 'status')
```

---

## 🎓 Learning Resources

- **Django Docs**: https://docs.djangoproject.com/
- **Django ORM**: https://docs.djangoproject.com/en/6.0/topics/db/
- **Models**: https://docs.djangoproject.com/en/6.0/topics/db/models/
- **Queries**: https://docs.djangoproject.com/en/6.0/topics/db/queries/
- **Database**: https://docs.djangoproject.com/en/6.0/topics/db/

---

## ✨ Summary

Most issues can be solved by:
1. ✅ Checking terminal for error messages
2. ✅ Running database tests: `python test_database.py`
3. ✅ Restarting server: Ctrl+C, then `python manage.py runserver`
4. ✅ Checking permissions in admin
5. ✅ Verifying database with: `python manage.py shell`

**If stuck**, run the reset:
```powershell
python setup_database.py
python manage.py migrate
python manage.py runserver
```

**You got this! 🚀**
