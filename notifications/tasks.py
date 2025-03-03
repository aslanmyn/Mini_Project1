from celery import shared_task
from django.utils.timezone import now
from users.models import User
from .models import Notification

@shared_task
def send_notification(user_id, message):
    user = User.objects.get(id=user_id)
    
    # Save notification to the database
    Notification.objects.create(
        user=user,
        message=message,
        timestamp=now()
    )

    return f"Notification sent to {user.username}"