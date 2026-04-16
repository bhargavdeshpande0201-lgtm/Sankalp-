# 🔧 SANKALP - Troubleshooting Guide

## Quick Fix Index

- [Server Issues](#-server-issues)
- [Database Issues](#-database-issues)
- [Import/Dependency Issues](#-importdependency-issues)
- [Static Files Issues](#-static-files-issues)
- [Authentication Issues](#-authentication-issues)
- [Template/Display Issues](#-templatedisplay-issues)
- [File Upload Issues](#-file-upload-issues)

---

## 🖥️ Server Issues

### Issue: "Port 8000 already in use"
**Error**: `Error: That port is already in use.`

**Solution**:
```bash
# Option 1: Run on different port
python manage.py runserver 0.0.0.0:8001

# Option 2: Kill process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Option 3: Kill process using port 8000 (Unix/Linux)
lsof -i :8000
kill -9 <PID>
```

---

### Issue: "ModuleNotFoundError: No module named 'django'"
**Error**: `ModuleNotFoundError: No module named 'django'`

**Solution**:
```bash
# 1. Activate virtual environment FIRST
venv\Scripts\activate          # Windows
source venv/bin/activate       # Unix/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
pip list | grep -i django
```

---

### Issue: Server returns "Page not found" (404)
**Error**: `Page not found (404)` on all URLs

**Solution**:
```bash
# 1. Check URLs are correct
# Access: http://127.0.0.1:8000/

# 2. Check app is in INSTALLED_APPS
# In sankalp/settings.py:
# 'core' should be in INSTALLED_APPS

# 3. Check views are properly defined
python manage.py shell
>>> from core.views import index
# Should not show ImportError
```

---

## 💾 Database Issues

### Issue: "No such table: core_complaint"
**Error**: `OperationalError: no such table: core_complaint`

**Solution**:
```bash
# Run migrations
python manage.py migrate

# If still fails, reset database
python manage.py migrate --run-syncdb

# Check migration status
python manage.py showmigrations
```

---

### Issue: "Migration conflicts"
**Error**: `Conflicting migrations detected`

**Solution**:
```bash
# Option 1: Merge migrations
python manage.py makemigrations --merge

# Option 2: Reset and remigrate (WARNING: Deletes data)
rm db.sqlite3
python manage.py migrate

# Option 3: Clear specific migration
python manage.py migrate core zero
python manage.py migrate core
```

---

### Issue: Database is locked
**Error**: `database is locked`

**Solution**:
```bash
# 1. Stop all Python processes
# Close all terminal windows running Django

# 2. Delete lock file
rm .db-journal  (or db.sqlite3-journal)

# 3. Restart server
python manage.py runserver
```

---

## 📦 Import/Dependency Issues

### Issue: "No module named 'PIL'" (Image upload not working)
**Error**: `ModuleNotFoundError: No module named 'PIL'`

**Solution**:
```bash
# Install Pillow
pip install Pillow==10.1.0

# Verify
python -c "from PIL import Image; print('PIL installed')"
```

---

### Issue: Missing requirements
**Error**: Various `ModuleNotFoundError`

**Solution**:
```bash
# Reinstall all requirements
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Verify each dependency
python -c "import django; print(django.VERSION)"
python -c "import PIL; print(PIL.__version__)"
```

---

## 📁 Static Files Issues

### Issue: CSS/JavaScript not loading (404 errors)
**Error**: Static files return 404

**Solution**:
```bash
# 1. Check settings.py has correct paths
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. For production, use whitenoise
pip install whitenoise
# Then add to MIDDLEWARE in settings.py:
# 'whitenoise.middleware.WhiteNoiseMiddleware'
```

---

### Issue: Images not uploading
**Error**: Image upload fails silently or shows file error

**Solution**:
```bash
# 1. Check media directory exists/permissions
# Create media/ folder in project root
mkdir media
mkdir media/complaints

# 2. Verify settings.py has:
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# 3. Check urls.py includes media URLs:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 4. Restart server
```

---

## 🔐 Authentication Issues

### Issue: "Login credentials not working"
**Error**: "Invalid username or password" for all accounts

**Solution**:
```bash
# 1. Create test user
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('testuser', 'test@test.com', 'password123')
>>> exit()

# 2. Try logging in with credentials
# Username: testuser
# Password: password123

# 3. If still failing, delete and recreate database
rm db.sqlite3
python manage.py migrate
```

---

### Issue: "Access denied" / "Permission denied"
**Error**: Staff/Admin features give permission errors

**Solution**:
```bash
# 1. Check if user is staff
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='username')
>>> user.is_staff
False  # Should be True for staff

# 2. Make user staff
>>> user.is_staff = True
>>> user.save()

# 3. Make user admin (superuser)
>>> user.is_superuser = True
>>> user.save()

# 4. Try accessing admin panel
# http://127.0.0.1:8000/admin-dashboard
```

---

### Issue: "Logout not working / Session issues"
**Error**: User stays logged in even after logout

**Solution**:
```bash
# 1. Clear browser cookies
# Settings → Privacy/Security → Clear browsing data → Cookies

# 2. Use incognito/private mode
# Browser specific shortcuts: Ctrl+Shift+N (Chrome), Ctrl+Shift+P (Firefox)

# 3. Restart server
# Sometimes session cache needs refresh

# 4. Check SESSION_COOKIE_AGE in settings.py
# Default is 2 weeks - can be reduced for development
SESSION_COOKIE_AGE = 3600  # 1 hour
```

---

## 🎨 Template/Display Issues

### Issue: "TemplateDoesNotExist" error
**Error**: `TemplateDoesNotExist: xxx.html`

**Solution**:
```bash
# 1. Verify file exists
# Check core/templates/ folder for the file

# 2. Check settings.py TEMPLATES configuration:
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'core' / 'templates'],
        # ...
    }
]

# 3. Verify app is in INSTALLED_APPS
# 'core' should be listed

# 4. Restart server
```

---

### Issue: "Variables not showing in template"
**Error**: Template shows {{ variable }} instead of value

**Solution**:
```bash
# 1. Check context in views.py
# View should include: context = {'variable': value}

# 2. Check template spelling
# {{ pending_count }} not {{ pending-count }}
# Hyphens not underscores

# 3. Verify template extends base.html
# {% extends 'base.html' %}

# 4. Check for typos in context keys
python manage.py shell
>>> from core.views import dashboard
# Review source code for exact variable names
```

---

### Issue: Form validation not working
**Error**: Form submits without validation or validation messages don't show

**Solution**:
```bash
# 1. Check form has CSRF token
# {% csrf_token %} in form

# 2. Check form method is POST
# <form method="POST">

# 3. Check views.py validates input
# Check for validation messages

# 4. Verify JavaScript is loaded
# Check browser console (F12 → Console)
```

---

## 📤 File Upload Issues

### Issue: "Image not saving / Upload fails silently"
**Error**: File upload shows success but image doesn't appear

**Solution**:
```bash
# 1. Check permissions on media folder
# chmod 755 media/  (Unix/Linux)

# 2. Check file size limits
# MAX_UPLOAD_SIZE = 5MB in settings.py
# FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

# 3. Check image format
# Only JPG, PNG, GIF, WebP supported

# 4. Verify database has permission to access media files
# Restart server with proper permissions
```

---

### Issue: "413 Payload Too Large"
**Error**: Large file upload fails

**Solution**:
```bash
# Increase upload limit in settings.py:
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Restart server
```

---

## 🔍 Debugging Tips

### Enable Debug Mode
```python
# In settings.py (DEVELOPMENT ONLY)
DEBUG = True
ALLOWED_HOSTS = ['*']
```

### Check Logs
```bash
# Django logs to console
# Watch for error messages during requests

# Check with verbose output
python manage.py runserver --verbosity=3
```

### Use Django Shell
```bash
python manage.py shell

# Test imports
>>> from core.models import Complaint
>>> Complaint.objects.all()
<QuerySet []>

# Test views
>>> from core.views import index
>>> index

# Test user creation
>>> from django.contrib.auth.models import User
>>> user = User.objects.first()
>>> user.username
```

### Check Django System
```bash
python manage.py check
python manage.py check --deploy  # Production check
```

---

## 📞 Getting Help

### Resources
1. **Django Documentation**: https://docs.djangoproject.com/
2. **Python Documentation**: https://docs.python.org/3/
3. **Bootstrap Documentation**: https://getbootstrap.com/docs/
4. **Pillow (Image) Docs**: https://pillow.readthedocs.io/

### Debugging Steps
1. Read the error message completely
2. Check the file and line number mentioned
3. Look for the exact error in documentation
4. Test components in isolation (Django shell)
5. Check browser console (F12) for frontend errors
6. Review recent changes if it worked before

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `ModuleNotFoundError` | Package not installed | `pip install <package>` |
| `TemplateDoesNotExist` | HTML file not found | Check template path |
| `OperationalError` | Database issue | Run migrations |
| `PermissionError` | Access denied | Check user role |
| `404 Not Found` | URL doesn't exist | Check urls.py |
| `500 Internal Error` | Code error | Check logs/console |

---

## 🎯 Frequently Asked Questions

### Q: How do I reset the database?
A: Delete `db.sqlite3` and run `python manage.py migrate`

### Q: How do I create demo data?
A: Use Django shell:
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('demo', 'demo@test.com', 'demo123')
```

### Q: How do I change the SECRET_KEY?
A: In `sankalp/settings.py`, generate a new one using:
```python
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

### Q: Can I use PostgreSQL instead of SQLite?
A: Yes, update DATABASES in settings.py and install `psycopg2-binary`

### Q: How do I deploy to production?
A: Follow Django deployment guide: https://docs.djangoproject.com/en/6.0/howto/deployment/

---

**Last Updated**: April 11, 2026  
**Version**: 1.0.0
