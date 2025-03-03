from rest_framework import serializers
from .models import Order, Transaction

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'product', 'quantity', 'status', 'created_at']
        
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['order', 'status', 'payment_method', 'amount', 'transaction_id', 'timestamp']