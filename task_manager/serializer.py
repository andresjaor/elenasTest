from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    creation_date = serializers.DateTimeField(required=False)
    is_done = serializers.BooleanField(required=False)
    description = serializers.CharField(required=True, allow_blank=False)


class PaginatorTaskSerializer(serializers.Serializer):
    num_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()