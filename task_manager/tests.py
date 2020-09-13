from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from task_manager.models import Task


class ApiAuthTest(TestCase):
    def test_authentication(self):
        # create initial_data
        if not User.objects.filter(username="username1").exists():
            user = User.objects.create_user("username1", "username1@admin.com", "Pass_username1")
            Task.objects.create(user=user, description="test message")
        client = APIClient()
        response = client.post(reverse('auth_token'), {'username': "username1", 'password': "Pass_username1"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.data.get('token'), None)
        response = client.post(reverse('auth_token'), {'username': "asdfgh1", 'password': "dfghjk"})
        self.assertEqual(response.status_code, 400)


class ApiTaskTest(TestCase):

    def test_task_pagination(self):
        # create initial_data
        if not User.objects.filter(username="username1").exists():
            user = User.objects.create_user("username1", "username1@admin.com", "Pass_username1")
            for n in range(100):
                Task.objects.create(user=user, description=f"test message {n}")
        client = APIClient()
        response = client.post(reverse('auth_token'), {'username': "username1", 'password': "Pass_username1"})
        token = response.data['token']
        response = client.get(reverse('task_resource'), HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.data['paginator'], None)
        self.assertEquals(response.data['paginator']['num_pages'], 10)
