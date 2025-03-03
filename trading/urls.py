from django.conf import settings
from django.urls import path, include
from .views import OrderAPI, TransactionAPI, create_trade_request, confirm_trade, accept_trade, decline_trade
from django.conf.urls.static import static 
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'orders', OrderAPI)
router.register(r'transactions', TransactionAPI)

urlpatterns = [
    path('trade/create/<int:product_id>/', create_trade_request, name='create_trade_request'),
    path("trade/accept/<int:trade_id>/", accept_trade, name="accept_trade"),
    path("trade/decline/<int:trade_id>/", decline_trade, name="decline_trade"),
    path('trade/confirm/<int:trade_id>/', confirm_trade, name='confirm_trade'),
    path('api/', include(router.urls)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

