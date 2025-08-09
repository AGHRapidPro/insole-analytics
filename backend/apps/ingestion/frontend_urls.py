from django.urls import path
from .views import UploadCSVView

urlpatterns = [
    path('', UploadCSVView.as_view(), name='upload'),
]
