import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sankalp.settings')
django.setup()

from django.contrib.auth.models import User

print("=" * 60)
print("  SANKALP - DATABASE SETUP")
print("=" * 60)

# Create superuser if doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sankalp.com', 'admin@2024')
    print("\n✅ Superuser created successfully!")
    print("\n   LOGIN CREDENTIALS:")
    print("   ─" * 20)
    print("   Username: admin")
    print("   Password: admin@2024")
    print("   ─" * 20)
else:
    print("\nℹ️  Admin superuser already exists")

# Create some demo staff/teacher accounts
demo_staff = [
    ('teacher1', 'teacher@sankalp.com', 'Teacher@123'),
    ('teacher2', 'teacher2@sankalp.com', 'Teacher@123'),
]

for username, email, password in demo_staff:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, email, password)
        user.is_staff = True
        user.save()
        print(f"   ✅ Staff account '{username}' created")
    else:
        print(f"   ℹ️  Staff account '{username}' already exists")

# Create some demo student accounts
demo_students = [
    ('student1', 'student1@sankalp.com', 'Student@123'),
    ('student2', 'student2@sankalp.com', 'Student@123'),
]

for username, email, password in demo_students:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username, email, password)
        print(f"   ✅ Student account '{username}' created")
    else:
        print(f"   ℹ️  Student account '{username}' already exists")

# Display all users
print("\n" + "=" * 60)
print("  ALL USERS IN DATABASE:")
print("=" * 60)
for user in User.objects.all().order_by('-date_joined'):
    role = "SUPERUSER" if user.is_superuser else "STAFF" if user.is_staff else "STUDENT"
    print(f"   {user.username:<15} | {role:<12} | {user.email}")

print("\n" + "=" * 60)
print(f"  Total Users: {User.objects.count()}")
print("=" * 60)
print("\n✨ Database setup complete!\n")
