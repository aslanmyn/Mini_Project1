from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import register, ProfileView, ProfileUpdateView, ProfileDeleteView, UserViewSet
from django.contrib.auth.views import LoginView, LogoutView


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('api/drf-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<str:username>/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('api/', include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)