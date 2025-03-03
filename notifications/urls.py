from django.urls import path
from notifications.views import dashboard

urlpatterns = [
    path('fetch/', dashboard, name='fetch_notifications'),
]
