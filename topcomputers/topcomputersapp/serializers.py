from rest_framework import serializers
from .models import StoredFile

class StoredFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StoredFile
        fields = [
            'id',
            'title',
            'description',
            'file',
            'file_url',
            'file_size_mb',
            'file_type',
            'file_extension',
            'is_image',
            'uploaded_at',
            'likes_count',
            'comments_count',
        ]
        read_only_fields = ['file_size_mb', 'file_type', 'file_extension', 'is_image', 'uploaded_at', 'file_url', 'likes_count', 'comments_count']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file:
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

    def get_comments_count(self, obj):
        return obj.comments.count()

    # Removed size validation
    def validate_file(self, value):
        return value
