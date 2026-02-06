from django.contrib import admin
from .models import StoredFile, FileComment, Contact
from django.utils.html import format_html

@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_preview', 'file_type', 'file_extension', 'file_size_mb', 'likes_count', 'comments_count', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at', 'is_image')
    search_fields = ('title', 'description', 'file_extension')
    readonly_fields = ('file_size_mb', 'file_type', 'file_extension', 'is_image', 'file_preview', 'likes_count')

    # Show image thumbnail if file is image
    def file_preview(self, obj):
        if obj.is_image:
            return format_html('<img src="{}" width="100" style="object-fit: cover;" />', obj.file.url)
        else:
            return format_html('<a href="{}">Download</a>', obj.file.url)

    def comments_count(self, obj):
        return obj.comments.count()
    
    comments_count.short_description = 'Comments'
    file_preview.short_description = 'Preview'


@admin.register(FileComment)
class FileCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('comment_text', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('created_at', 'is_read')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'name', 'email', 'subject', 'message')
    
    def has_add_permission(self, request):
        return False
