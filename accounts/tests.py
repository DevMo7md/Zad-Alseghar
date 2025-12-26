from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
# temp
User = get_user_model()

class LoginTest(TestCase):
    def test_login_error(self):
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        client = APIClient()
        response = client.post('/api/accounts/token/', {'username': 'admin', 'password': 'admin'}, format='json')
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(response.content.decode()) # This will show up in test output
        self.assertEqual(response.status_code, 200)
