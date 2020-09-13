from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from task_manager.views import TaskResource

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', views.obtain_auth_token, name='auth_token'),
    path(r'task/', TaskResource.as_view(), name='task_resource')
]
