from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

@login_required
def dashboard(request):
    # Fetch only the logged-in user's latest 10 notifications
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:10]
    
    return render(request, 'notifications/notificate.html', {'notifications': notifications})