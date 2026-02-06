from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import os
import mimetypes
from .storages import ProductStorage

User = get_user_model()


class StoredFile(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    file = models.FileField(storage=ProductStorage())

    file_size_mb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    file_type = models.CharField(max_length=100, editable=False)  # MIME
    file_extension = models.CharField(max_length=10, editable=False)

    is_image = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_files', blank=True)

    # 🔒 size validation removed
    def clean(self):
        pass  # No validation now

    def save(self, *args, **kwargs):
        if self.file:
            # size MB
            self.file_size_mb = round(self.file.size / (1024 * 1024), 2)

            # extension
            self.file_extension = os.path.splitext(self.file.name)[1].lower()

            # MIME type
            self.file_type, _ = mimetypes.guess_type(self.file.name)
            self.file_type = self.file_type or "unknown"

            # image detect
            self.is_image = self.file_type.startswith("image/")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class FileComment(models.Model):
    file = models.ForeignKey(StoredFile, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.file.title}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"
