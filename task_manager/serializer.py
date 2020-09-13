from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)
    creation_date = serializers.DateTimeField(required=False)
    is_done = serializers.BooleanField(required=False)
    description = serializers.CharField(required=True, allow_blank=False)


class PaginatorTaskSerializer(serializers.Serializer):
    num_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()


class UpdateTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    is_done = serializers.BooleanField(required=True)