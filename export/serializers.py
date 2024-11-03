from rest_framework import serializers


class ExportRequestSerializer(serializers.Serializer):
    queue_id = serializers.CharField(max_length=50)
    annotation_id = serializers.CharField(max_length=50)
