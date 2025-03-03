"""
URL configuration for sales_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, include
from users.views import homepage
from users.permissions import IsAdmin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Sales and Trading API",
        default_version="v1",
        description="API documentation for Sales and Trading project",
        terms_of_service="https://www.yoursite.com/terms/",
        contact=openapi.Contact(email="support@yoursite.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(IsAdmin,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='home'),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('trading/', include('trading.urls')),
    path('sales/', include('sales.urls')),
    path('notifications/', include('notifications.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

