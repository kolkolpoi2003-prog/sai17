
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.db import IntegrityError

try:
    # Create a user without profile
    user_name = 'test_reproduce_user'
    if User.objects.filter(username=user_name).exists():
        User.objects.filter(username=user_name).delete()
    
    user = User.objects.create_user(username=user_name, password='password')
    print(f"User {user.username} created.")

    # Try to create profile without fields
    print("Attempting to create UserProfile with only user field...")
    try:
        profile = UserProfile.objects.create(user=user)
        print("UserProfile created successfully.")
    except Exception as e:
        print(f"FAILED to create UserProfile: {e}")

except Exception as e:
    print(f"Global error: {e}")
