import stripe
import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Invoice, SalesOrder
from products.models import Product
from rest_framework import viewsets
from .serializers import InvoiceSerializer, SalesOrderSerializer
from users.permissions import IsAdmin
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from decimal import Decimal
from notifications.tasks import send_notification


stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()

def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(float(product.price.replace("$", "").strip()) * 100),  # Convert to cents
                'product_data': {
                    'name': product.name,
                    'description': product.description,
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"http://127.0.0.1:8000/sales/payment-success/{product.id}/",
        cancel_url=f"http://127.0.0.1:8000/sales/payment-cancel/",
    )

    return redirect(checkout_session.url)  # Redirect user to Stripe checkout


def payment_success(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    product = get_object_or_404(Product, id=product_id)
    customer = User.objects.get(id=request.user.id)

    # Convert product price to Decimal (remove '$' sign if present)
    price_decimal = Decimal(product.price.replace("$", "").strip())

    # Create SalesOrder
    sales_order = SalesOrder.objects.create(
        customer=customer,
        status="paid",
        total_amount=price_decimal,  # Use converted decimal value
    )

    # Generate Invoice
    invoice = Invoice.objects.create(
        sales_order=sales_order,
        invoice_number=str(uuid.uuid4())[:10],  # Unique Invoice Number
        due_date=now() + timedelta(days=7),
        paid=True,
    )

    # ✅ Send Notification (Async with Celery)
    send_notification.delay(
        user_id=customer.id,
        message=f"Your purchase of {product.name} was successful! 🎉"
    )

    context = {
        'sales_order': sales_order,
        'invoice': invoice,
        'product': product,
    }

    return render(request, 'payment/payment_successful.html', context)


def generate_invoice_pdf(request, order_id):
    invoice = get_object_or_404(Invoice, sales_order__id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Invoice Number: {invoice.invoice_number}")
    p.drawString(100, 780, f"Sales Order ID: {invoice.sales_order.id}")
    p.drawString(100, 760, f"Customer: {invoice.sales_order.customer.username}")
    p.drawString(100, 740, f"Total Amount: ${invoice.sales_order.total_amount}")
    p.drawString(100, 720, f"Issued Date: {invoice.issued_date.strftime('%Y-%m-%d')}")
    p.drawString(100, 700, f"Due Date: {invoice.due_date.strftime('%Y-%m-%d')}")
    p.drawString(100, 680, f"Status: {'Paid' if invoice.paid else 'Unpaid'}")

    p.showPage()
    p.save()

    return response



class InvoiceAPI(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAdmin]
    
    
class SalesOrderAPI(viewsets.ModelViewSet):
    serializer_class = SalesOrderSerializer
    queryset = SalesOrder.objects.all()
    permission_classes = [IsAdmin]
    
    



