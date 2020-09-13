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
    def create_initial_data(num_tasks=100, username=1):
        # create initial_data
        if not User.objects.filter(username=f"username{username}").exists():
            user = User.objects.create_user(f"username{username}",
                                            f"username{username}@admin.com", f"Pass_username{username}")
            tasks = []
            for n in range(num_tasks):
                task = Task.objects.create(user=user, description=f"test message {n}")
                tasks.append(task)
            return user, tasks

    @staticmethod
    def generate_auth_token(username=1):
        client = APIClient()
        response = client.post(reverse('auth_token'), {'username': f"username{username}",
                                                       'password': f"Pass_username{username}"})
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
        response = client.put(reverse('task_resource'), data={"id": 1, "is_done": True, "description": "New"},
                              HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)
        db_task = Task.objects.get(id=1)
        self.assertEqual(db_task.is_done, True)
        response = client.put(reverse('task_resource'), data={"id": 1, "is_done": False, "description": "New"},
                              HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 200)
        db_task = Task.objects.get(id=1)
        self.assertEqual(db_task.is_done, False)
        self.assertEqual(db_task.description, "New")
        # testing private tasks
        self.create_initial_data(1, 2)
        token = self.generate_auth_token(2)
        response = client.put(reverse('task_resource'), data={"id": 1, "is_done": False},
                              HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, 403)

    def test_delete_task(self):
        self.create_initial_data(1)
        token_1 = self.generate_auth_token()
        client = APIClient()
        response = client.delete(reverse('task_resource'), data={}, HTTP_AUTHORIZATION=f'Token {token_1}')
        self.assertEqual(response.status_code, 400)
        response = client.delete(reverse('task_resource'), data={"id": 1},
                                 HTTP_AUTHORIZATION=f'Token {token_1}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.filter(id=1).first(), None)
        # testing private tasks
        self.create_initial_data(1, 2)
        response = client.delete(reverse('task_resource'), data={"id": 2},
                                 HTTP_AUTHORIZATION=f'Token {token_1}')
        self.assertEqual(response.status_code, 403)
