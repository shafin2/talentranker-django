from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin user'

    def handle(self, *args, **options):
        email = 'admin@talentranker.com'
        password = 'admin123'
        name = 'Admin User'
        
        # Check if admin already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Admin user {email} already exists'))
            return
        
        # Create admin user
        admin_user = User.objects.create_superuser(
            email=email,
            password=password,
            name=name
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Admin user created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
        self.stdout.write(self.style.WARNING('⚠️  Please change the password after first login!'))
