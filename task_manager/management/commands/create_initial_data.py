# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from task_manager.models import Task

INITIAL_MESSAGE = "Hi {0}! Your first task will be to create a new task"


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "admin")

        if not User.objects.filter(username="username1").exists():
            user1 = User.objects.create_user("username1", "username1@admin.com", "Pass_username1", is_active=True)
            Task.objects.create(user=user1, description=INITIAL_MESSAGE.format(user1.username))

        if not User.objects.filter(username="username2").exists():
            user2 = User.objects.create_user("username2", "username2@admin.com", "Pass_username2", is_active=True)
            Task.objects.create(user=user2, description=INITIAL_MESSAGE.format(user2.username))
        print("ok!")

