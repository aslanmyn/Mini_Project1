from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static 
from rest_framework import routers
from .views import SalesOrderAPI, InvoiceAPI, create_checkout_session, payment_success, generate_invoice_pdf

router = routers.SimpleRouter()
router.register(r'sales_orders', SalesOrderAPI)
router.register(r'invoices',InvoiceAPI)


urlpatterns = [
    path('api/', include(router.urls)),
    path('create-checkout-session/<int:product_id>/', create_checkout_session, name='create_checkout_session'),
    path('payment-success/<int:product_id>/', payment_success, name='payment_success'),
    path('invoice/<int:order_id>/', generate_invoice_pdf, name='generate_invoice_pdf'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

