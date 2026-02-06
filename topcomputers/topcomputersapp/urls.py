from django import views
from .views import StoredFileListCreateAPIView, home_view, get_files_api, like_file, add_comment, contact_submit, file_detail
from django.urls import path
from .views import file_detail
urlpatterns = [
    path('home/', home_view, name='home'),
     path('file/<int:file_id>/', file_detail, name='file_detail'),
    path('api/files/', StoredFileListCreateAPIView.as_view(), name='storedfile-list-create'),
    path('api/files-signed/', get_files_api, name='get_files_api'),
    path('like/<int:file_id>/', like_file, name='like_file'),
    path('comment/<int:file_id>/', add_comment, name='add_comment'),
    path('contact/submit/', contact_submit, name='contact_submit'),
    
]
