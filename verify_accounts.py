import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zadProject.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()
client = APIClient()

def run_verification():
    print("--- Starting Verification ---")
    
    # Check User
    if not User.objects.filter(username='admin').exists():
        print("User 'admin' not found. Creating...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    else:
        print("User 'admin' found.")

    # 1. Register New User
    import uuid
    new_username = f"user_{uuid.uuid4().hex[:6]}"
    print(f"\n1. Testing Register New User ({new_username})...")
    reg_data = {
        'username': new_username,
        'password': 'password123',
        'email': f'{new_username}@example.com'
    }
    response = client.post('/api/accounts/register/', reg_data, format='json')
    if response.status_code == 201:
        print("Registration Successful!")
        # Tokens are returned, use them to test logout later
        user_refresh = response.data['refresh']
        user_access = response.data['access']
    else:
        print(f"Registration Failed: {response.status_code}")
        if hasattr(response, 'data'): print(response.data)

    # 2. Login (Admin)
    print("\n2. Testing Login (Admin)...")
    response = client.post('/api/accounts/token/', {'username': 'admin', 'password': 'admin'}, format='json')
    if response.status_code == 200:
        print("Login Successful!")
        access_token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    else:
        print(f"Login Failed: {response.status_code}")
        if hasattr(response, 'data'):
            print(response.data)
        else:
            print(response.content.decode()[:500]) # First 500 chars
        return

    # 2. Create Contact Message
    print("\n2. Testing Create Contact Message...")
    msg_data = {'subject': 'Hello Admin', 'message': 'This is a test message.'}
    response = client.post('/api/accounts/contact/', msg_data, format='json')
    if response.status_code == 201:
        print("Message Created Successfully!")
    else:
        print(f"Message Creation Failed: {response.status_code} {response.data}")

    # 3. List Contact Messages
    print("\n3. Testing List Contact Messages...")
    response = client.get('/api/accounts/contact/')
    if response.status_code == 200:
        print(f"Found {len(response.data)} messages.")
    else:
        print(f"List Messages Failed: {response.status_code}")

    # 4. Record View
    # Use ContactMessage as a dummy content object since it has integer ID
    from accounts.models import ContactMessage
    from django.contrib.contenttypes.models import ContentType
    
    # Create a dummy message to view (if not exists)
    if not ContactMessage.objects.filter(subject='Test View').exists():
         # We need a user to create a message. Admin is already there.
         admin_user = User.objects.get(username='admin')
         ContactMessage.objects.create(user=admin_user, subject='Test View', message='Content to view')
    
    target_msg = ContactMessage.objects.filter(subject='Test View').first()
    target_ct_name = 'contactmessage' # model name

    print("\n4. Testing Record View (Generic)...")
    view_data = {'model_name': target_ct_name, 'object_id': target_msg.id}
    response = client.post('/api/accounts/record-view/', view_data, format='json')
    if response.status_code == 201:
        print("View Recorded Successfully!")
    else:
        print(f"View Record Failed: {response.status_code}")
        if hasattr(response, 'data'):
            print(response.data)

    # 5. Check Dashboard Stats
    print("\n5. Testing Dashboard Stats (Admin)...")
    response = client.get('/api/accounts/dashboard/stats/')
    if response.status_code == 200:
        print("Dashboard Stats Retrieved:")
        print(response.data)
    else:
        print(f"Dashboard Stats Failed: {response.status_code}")

    # 6. Logout
    print("\n6. Testing Logout...")
    if 'user_refresh' in locals():
        # Logout the registered user
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_access)
        response = client.post('/api/accounts/logout/', {'refresh': user_refresh}, format='json')
        if response.status_code == 205:
            print("Logout Successful!")
        else:
            print(f"Logout Failed: {response.status_code}")
            if hasattr(response, 'data'): print(response.data)
    else:
        print("Skipping logout test as registration failed.")

    # 7. Test Permission (Create Content as regular user)
    print("\n7. Testing Permission (Create Content as Regular User)...")
    if 'user_access' in locals():
         client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_access)
         # Try to create a ContactMessage (Allowed)
         response = client.post('/api/accounts/contact/', {'subject': 'User Msg', 'message': 'Test'}, format='json')
         if response.status_code == 201:
             print("User allowed to create Contact Message (Correct).")
         else:
             print(f"User failed to create Contact Message: {response.status_code}")

         # Try to create a Video in Prophets (Should fail)
         # Assuming /api/prophets/videos/ exists
         response = client.post('/api/prophets/videos/', {'title': 'Hack Video', 'youtube_link': '...'}, format='json')
         if response.status_code == 403:
             print("User DENIED creating Video (Correct).")
         else:
             print(f"User result for creating Video: {response.status_code} (Expected 403)")

if __name__ == '__main__':
    run_verification()
