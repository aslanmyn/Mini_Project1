from django.contrib import admin
from .models import Invoice, SalesOrder

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at', 'total_amount')
    search_fields = ('customer', )
    

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('sales_order', 'invoice_number', 'issued_date', 'due_date', 'paid')
    search_fields = ('invoice_number', )