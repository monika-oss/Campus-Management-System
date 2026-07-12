import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from faculty.models import Faculty
from students.models import Student
from authentication.models import User

print("--- Syncing Faculty Users ---")
for f in Faculty.objects.all():
    print(f"Faculty: {f.name} ({f.email})")
    
    # If the user is linked but the email doesn't match, or if the user is not linked
    user_with_email = User.objects.filter(email=f.email).first()
    
    if f.user:
        # Check if the linked user's email matches the faculty email
        if f.user.email != f.email:
            print(f"  Linked user email ({f.user.email}) does not match faculty email ({f.email})")
            if user_with_email:
                # If a user already exists with the faculty's email, link to that user
                print(f"  User with email {f.email} already exists. Linking to that user.")
                # If the current linked user is a dummy or not used, we can keep it or delete it if it's not linked to anything else
                old_user = f.user
                f.user = user_with_email
                f.save()
                # Clean up old user if it has no other profile linked
                if not Faculty.objects.filter(user=old_user).exists() and not Student.objects.filter(user=old_user).exists():
                    print(f"  Deleting old unused user {old_user.email}")
                    old_user.delete()
            else:
                # Update the linked user's email to match the faculty's email
                print(f"  Updating linked user email from {f.user.email} to {f.email}")
                f.user.email = f.email
                f.user.set_password('faculty123')
                f.user.save()
        else:
            # Just ensure the password is 'faculty123' to make sure they can log in
            f.user.set_password('faculty123')
            f.user.save()
            print("  Password reset/verified to 'faculty123'")
    else:
        # No user linked, look for user with email or create new
        if user_with_email:
            print(f"  Found existing user with email {f.email}. Linking.")
            f.user = user_with_email
            f.save()
        else:
            print(f"  Creating new user for {f.email}")
            new_user = User.objects.create_user(
                email=f.email,
                password='faculty123',
                name=f.name,
                role='faculty'
            )
            f.user = new_user
            f.save()

print("\n--- Syncing Student Users ---")
for s in Student.objects.all():
    print(f"Student: {s.name} ({s.email})")
    user_with_email = User.objects.filter(email=s.email).first()
    
    if s.user:
        if s.user.email != s.email:
            print(f"  Linked user email ({s.user.email}) does not match student email ({s.email})")
            if user_with_email:
                print(f"  User with email {s.email} already exists. Linking to that user.")
                old_user = s.user
                s.user = user_with_email
                s.save()
                if not Faculty.objects.filter(user=old_user).exists() and not Student.objects.filter(user=old_user).exists():
                    print(f"  Deleting old unused user {old_user.email}")
                    old_user.delete()
            else:
                print(f"  Updating linked user email from {s.user.email} to {s.email}")
                s.user.email = s.email
                s.user.set_password('student123')
                s.user.save()
        else:
            s.user.set_password('student123')
            s.user.save()
            print("  Password reset/verified to 'student123'")
    else:
        if user_with_email:
            print(f"  Found existing user with email {s.email}. Linking.")
            s.user = user_with_email
            s.save()
        else:
            print(f"  Creating new user for {s.email}")
            new_user = User.objects.create_user(
                email=s.email,
                password='student123',
                name=s.name,
                role='student'
            )
            s.user = new_user
            s.save()

print("\nSync completed successfully!")
