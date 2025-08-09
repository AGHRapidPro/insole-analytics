from django.urls import path
from django.http import JsonResponse

def ping(request):
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('ping/', ping, name='api-ping'),
]
