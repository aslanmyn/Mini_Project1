from rest_framework import serializers
from .models import SalesOrder, Invoice

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ['customer', 'status', 'created_at', 'total_amount']
        
        
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['sales_order', 'invoice_number', 'issued_date', 'due_date', 'paid']