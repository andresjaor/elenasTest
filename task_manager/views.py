from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from task_manager.models import Task
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from task_manager.serializer import TaskSerializer, PaginatorTaskSerializer, UpdateTaskSerializer


class AuthTokenResource(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        }, status=status.HTTP_200_OK)


class TaskResource(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_serializer_class = PaginatorTaskSerializer

    def get(self, request):
        page = self.request.query_params.get('page', 1)
        tasks_query = Task.objects.prefetch_related('user').only('id')\
            .filter(user=self.request.user).order_by('-creation_date')
        paginator = Paginator(tasks_query, settings.TASKS_PER_PAGE)
        setattr(paginator, 'current_page', page)
        pagination_serializer = self.pagination_serializer_class(paginator)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            return Response("page must be an integer", status.HTTP_400_BAD_REQUEST)
        except EmptyPage:
            return Response({'tasks': [], 'paginator': pagination_serializer.data}, status.HTTP_200_OK)
        data_serializer = self.serializer_class(tasks, many=True)
        return Response({'tasks': data_serializer.data, 'paginator': pagination_serializer.data})

    def post(self, request):
        task = self.serializer_class(data=self.request.data)
        task.is_valid(raise_exception=True)
        data = task.data
        task = Task.objects.create(user=self.request.user, description=data['description'])
        serializer = self.serializer_class(task)
        return Response(serializer.data)

    def put(self, request):
        update_task = UpdateTaskSerializer(data=request.data)
        update_task.is_valid(raise_exception=True)
        data = update_task.data
        try:
            task = Task.objects.get(id=data['id'])
            task.is_done = data['is_done']
            task.save()
        except Task.DoesNotExist:
            return Response(f"task with id={data['id']} not found", status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(task)
        return Response(serializer.data)

    def delete(self, request):
        task_id = self.request.data.get('id')
        if not task_id:
            return Response(f"id param is mandatory", status.HTTP_400_BAD_REQUEST)
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
        except Task.DoesNotExist:
            return Response(f"task with id={task_id} not found", status.HTTP_400_BAD_REQUEST)
        return Response({"task": task_id}, status.HTTP_200_OK)


