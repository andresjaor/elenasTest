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
    @staticmethod
    def create_initial_data(num_tasks=100):
        # create initial_data
        if not User.objects.filter(username="username1").exists():
            user = User.objects.create_user("username1", "username1@admin.com", "Pass_username1")
            tasks = []
            for n in range(num_tasks):
                task = Task.objects.create(user=user, description=f"test message {n}")
                tasks.append(task)
            return user, tasks

    @staticmethod
    def generate_auth_token():
        client = APIClient()
        response = client.post(reverse('auth_token'), {'username': "username1", 'password': "Pass_username1"})
        return response.data['token']

    def test_task_pagination(self):
        self.create_initial_data()
        token = self.generate_auth_token()
        client = APIClient()
        response = client.get(reverse('task_resource'), HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.data['paginator'], None)
        self.assertEquals(response.data['paginator']['num_pages'], 10)

    def test_insert_task(self):
        self.create_initial_data(0)
        token = self.generate_auth_token()
        client = APIClient()
        response = client.post(reverse('task_resource'), data={}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 400)
        response = client.post(reverse('task_resource'), data={"description": "This a test"},
                               HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.data, None)

    def test_update_task(self):
        self.create_initial_data(1)
        token = self.generate_auth_token()
        client = APIClient()
        response = client.put(reverse('task_resource'), data={}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 400)
        response = client.put(reverse('task_resource'), data={"id": 1, "is_done": True},
                              HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)
        db_task = Task.objects.get(id=1)
        self.assertEqual(db_task.is_done, True)
        response = client.put(reverse('task_resource'), data={"id": 1, "is_done": False},
                              HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)
        db_task = Task.objects.get(id=1)
        self.assertEqual(db_task.is_done, False)

    def delete_update_task(self):
        self.create_initial_data(1)
        token = self.generate_auth_token()
        client = APIClient()
        response = client.delete(reverse('task_resource'), data={}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 400)
        response = client.delete(reverse('task_resource'), data={"id": 1},
                                 HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)
        self.assertRaises(Task.DoesNotExist, Task.objects.get(id=1))
