from django.contrib import admin
from .models import Order, Transaction, TradeRequest

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'created_at')
    search_fields = ('user', )
    
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'payment_method', 'amount', 'transaction_id')
    search_fields = ('transaction_id', )
    
    
admin.site.register(TradeRequest)
