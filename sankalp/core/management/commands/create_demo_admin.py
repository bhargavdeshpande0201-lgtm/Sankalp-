from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create demo admin user for testing'

    def handle(self, *args, **options):
        # Create admin user if doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@sankalp.edu.in',
                password='Admin123456'
            )
            admin_user.first_name = 'Admin'
            admin_user.last_name = 'User'
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Demo admin user created successfully!\n'
                    'Username: admin\n'
                    'Password: Admin123456\n'
                    'Email: admin@sankalp.edu.in'
                )
            )
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create demo staff user
        if not User.objects.filter(username='staff1').exists():
            staff_user = User.objects.create_user(
                username='staff1',
                email='staff1@sankalp.edu.in',
                password='Staff123456',
                first_name='John',
                last_name='Teacher'
            )
            staff_user.is_staff = True
            staff_user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Demo staff user created!\n'
                    'Username: staff1\n'
                    'Password: Staff123456'
                )
            )

        # Create more staff users
        for i in range(2, 4):
            if not User.objects.filter(username=f'staff{i}').exists():
                staff_user = User.objects.create_user(
                    username=f'staff{i}',
                    email=f'staff{i}@sankalp.edu.in',
                    password='Staff123456',
                    first_name=f'Staff{i}',
                    last_name='Member'
                )
                staff_user.is_staff = True
                staff_user.save()

        self.stdout.write(self.style.SUCCESS('All demo users created!'))
