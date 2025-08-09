from django.urls import path
from .api_views import CSVUploadAPI

urlpatterns = [
    path('upload_csv/', CSVUploadAPI.as_view(), name='api-upload-csv'),
]
