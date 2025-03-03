from django.conf import settings
from django.urls import path, include
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductViewAPI, CategoryViewAPI
from django.conf.urls.static import static 
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products1', ProductViewAPI)
router.register(r'categories', CategoryViewAPI)


urlpatterns = [
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('api/', include(router.urls)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

