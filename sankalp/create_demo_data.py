"""
Populate SANKALP database with demo data for presentation
Run: python manage.py shell < create_demo_data.py
"""

from django.contrib.auth.models import User
from core.models import Complaint, Comment
from datetime import datetime, timedelta
import random

# Clear existing data (optional)
# User.objects.all().delete()
# Complaint.objects.all().delete()
# Comment.objects.all().delete()

print("=" * 60)
print("CREATING DEMO DATA FOR SANKALP PRESENTATION")
print("=" * 60)

# ====================== CREATE USERS ======================
print("\n[1] Creating Users...")

# Student users
students = [
    {'username': 'student1', 'email': 'student1@college.edu', 'password': 'password123', 'first_name': 'Raj', 'last_name': 'Kumar'},
    {'username': 'student2', 'email': 'student2@college.edu', 'password': 'password123', 'first_name': 'Priya', 'last_name': 'Singh'},
    {'username': 'student3', 'email': 'student3@college.edu', 'password': 'password123', 'first_name': 'Akhil', 'last_name': 'Verma'},
    {'username': 'student4', 'email': 'student4@college.edu', 'password': 'password123', 'first_name': 'Neha', 'last_name': 'Patel'},
    {'username': 'student5', 'email': 'student5@college.edu', 'password': 'password123', 'first_name': 'Vikram', 'last_name': 'Reddy'},
]

# Teacher/Staff users
staff = [
    {'username': 'teacher1', 'email': 'teacher1@college.edu', 'password': 'password123', 'first_name': 'Dr.', 'last_name': 'Sharma', 'is_staff': True},
    {'username': 'teacher2', 'email': 'teacher2@college.edu', 'password': 'password123', 'first_name': 'Prof.', 'last_name': 'Gupta', 'is_staff': True},
    {'username': 'staff1', 'email': 'staff@college.edu', 'password': 'password123', 'first_name': 'Admin', 'last_name': 'User', 'is_staff': True},
]

# Admin user
admin = {'username': 'admin', 'email': 'admin@college.edu', 'password': 'admin123', 'first_name': 'System', 'last_name': 'Admin'}

# Create students
student_objects = []
for student in students:
    user, created = User.objects.get_or_create(username=student['username'])
    if created:
        user.email = student['email']
        user.first_name = student['first_name']
        user.last_name = student['last_name']
        user.set_password(student['password'])
        user.save()
        print(f"   ✓ Created Student: {student['first_name']} {student['last_name']}")
    else:
        print(f"   - Student {student['first_name']} already exists")
    student_objects.append(user)

# Create staff
staff_objects = []
for staff_member in staff:
    user, created = User.objects.get_or_create(username=staff_member['username'])
    if created:
        user.email = staff_member['email']
        user.first_name = staff_member['first_name']
        user.last_name = staff_member['last_name']
        user.is_staff = True
        user.set_password(staff_member['password'])
        user.save()
        print(f"   ✓ Created Staff: {staff_member['first_name']} {staff_member['last_name']}")
    else:
        print(f"   - Staff {staff_member['first_name']} already exists")
    staff_objects.append(user)

# Create admin
admin_user, created = User.objects.get_or_create(username=admin['username'])
if created:
    admin_user.email = admin['email']
    admin_user.first_name = admin['first_name']
    admin_user.last_name = admin['last_name']
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.set_password(admin['password'])
    admin_user.save()
    print(f"   ✓ Created Admin: {admin['first_name']} {admin['last_name']}")
else:
    print(f"   - Admin already exists")

# ====================== CREATE COMPLAINTS ======================
print("\n[2] Creating Sample Complaints...")

complaint_data = [
    {
        'title': 'Overflowing dustbin near library entrance',
        'description': 'The dustbin near the main library entrance has been overflowing for 3 days. Garbage is scattered on the ground and it smells bad. This needs immediate attention as it affects the cleanliness of the campus.',
        'category': 'Waste',
        'location': 'Library Entrance',
        'priority': 'high',
        'status': 'Resolved'
    },
    {
        'title': 'Broken water tap in Boys hostel bathroom',
        'description': 'The water tap in Block A bathroom has been leaking continuously. Water is wasting and the floor is wet which is a safety hazard. Please repair it as soon as possible.',
        'category': 'Infrastructure',
        'location': 'Boys Hostel - Block A',
        'priority': 'medium',
        'status': 'In Progress'
    },
    {
        'title': 'Insufficient parking spaces in campus',
        'description': 'The parking lot is always full by 10 AM. Students and staff struggle to find parking spaces. The college should consider expanding the parking area or implementing a better parking management system.',
        'category': 'Parking',
        'location': 'Main Parking Lot',
        'priority': 'medium',
        'status': 'Pending'
    },
    {
        'title': 'Gate open during night hours - Security issue',
        'description': 'I observed that the main campus gate is left open till late evening(After 7 PM). This is a major security concern as unauthorized persons can enter the campus. Please ensure the gate is locked properly after college hours.',
        'category': 'Security',
        'location': 'Main Gate',
        'priority': 'high',
        'status': 'In Progress'
    },
    {
        'title': 'Broken benches in campus courtyard',
        'description': 'Several wooden benches in the courtyard are broken and need replacement. Some benches are missing slats and are dangerous to sit on. This affects the seating area for students.',
        'category': 'Infrastructure',
        'location': 'Campus Courtyard',
        'priority': 'low',
        'status': 'Pending'
    },
    {
        'title': 'Dead trees need to be removed',
        'description': 'There are several dead trees near the sports field that are not only ugly but also dangerous as branches might fall during storms. These should be removed and replaced with new saplings.',
        'category': 'Infrastructure',
        'location': 'Sports Field Area',
        'priority': 'medium',
        'status': 'Pending'
    },
    {
        'title': 'No proper lighting on the back road',
        'description': 'The back road leading to the hostel has very poor lighting. It becomes very dark after 6 PM which is a safety concern, especially for female students. Additional street lights should be installed.',
        'category': 'Security',
        'location': 'Back Road to Hostel',
        'priority': 'high',
        'status': 'Resolved'
    },
    {
        'title': 'Rats in the cafeteria',
        'description': 'I have seen rats in the cafeteria multiple times. This is a serious hygiene issue. The cafeteria should be cleaned thoroughly and pest control measures should be taken immediately.',
        'category': 'Waste',
        'location': 'Cafeteria',
        'priority': 'high',
        'status': 'In Progress'
    },
    {
        'title': 'Damaged road surface near entrance',
        'description': 'The road surface near the main entrance has large potholes. This is dangerous for vehicles and can cause accidents. The road should be repaired with proper asphalt.',
        'category': 'Infrastructure',
        'location': 'Main Entrance Road',
        'priority': 'medium',
        'status': 'Pending'
    },
    {
        'title': 'Lack of tree shade in waiting area',
        'description': 'The waiting area outside the office has no trees or shade. During summer, students have to wait in direct sunlight which is uncomfortable. A few shade trees would make it much better.',
        'category': 'Infrastructure',
        'location': 'Office Waiting Area',
        'priority': 'low',
        'status': 'Pending'
    },
]

complaint_objects = []
base_date = datetime.now() - timedelta(days=30)

for i, complaint in enumerate(complaint_data):
    # Use different students for each complaint
    user = student_objects[i % len(student_objects)]
    
    comp, created = Complaint.objects.get_or_create(
        user=user,
        title=complaint['title'],
        defaults={
            'description': complaint['description'],
            'category': complaint['category'],
            'location': complaint['location'],
            'priority': complaint['priority'],
            'status': complaint['status'],
        }
    )
    
    if created:
        # Set created_at to spread complaints over time
        comp.created_at = base_date + timedelta(days=i*3)
        comp.save()
        print(f"   ✓ Created: {complaint['title'][:50]}... by {user.get_full_name()}")
    else:
        print(f"   - Complaint already exists: {complaint['title'][:50]}...")
    
    complaint_objects.append(comp)

# ====================== CREATE COMMENTS ======================
print("\n[3] Creating Sample Comments...")

comment_templates = [
    'We have received your complaint and will look into it.',
    'The issue has been identified. We are working on a solution.',
    'The maintenance team has been assigned to this issue.',
    'Thank you for reporting this. It helps us improve the campus.',
    'This has been marked as high priority.',
    'We appreciate your patience. We will resolve this soon.',
    'The concerned department has been notified.',
    'Regular monitoring will be done for this issue.',
]

comment_count = 0
for complaint in complaint_objects[:8]:  # Add comments to first 8 complaints
    # Add staff response
    staff_member = staff_objects[random.randint(0, len(staff_objects)-1)]
    
    comments_to_add = random.randint(1, 3)
    for _ in range(comments_to_add):
        comment_text = random.choice(comment_templates)
        Comment.objects.get_or_create(
            complaint=complaint,
            user=staff_member,
            text=comment_text,
            is_staff=True,
            defaults={}
        )
        comment_count += 1

print(f"   ✓ Created {comment_count} staff comments")

# ====================== PRINT SUMMARY ======================
print("\n" + "=" * 60)
print("DEMO DATA CREATION COMPLETE!")
print("=" * 60)
print(f"\n✓ Users Created:")
print(f"  - Students: {len(student_objects)}")
print(f"  - Staff: {len(staff_objects)}")
print(f"  - Admin: 1")
print(f"\n✓ Total Users: {User.objects.count()}")
print(f"✓ Total Complaints: {Complaint.objects.count()}")
print(f"✓ Total Comments: {Comment.objects.count()}")

print(f"\n" + "=" * 60)
print("TEST CREDENTIALS:")
print("=" * 60)
print(f"\nStudent Account:")
print(f"  Username: student1")
print(f"  Password: password123")
print(f"\nStaff Account:")
print(f"  Username: teacher1")
print(f"  Password: password123")
print(f"\nAdmin Account:")
print(f"  Username: admin")
print(f"  Password: admin123")
print(f"\n" + "=" * 60)
print("Database is ready for presentation!")
print("=" * 60)
