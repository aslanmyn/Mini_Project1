from django.db import models
from users.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    
class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')], default='success')
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('crypto', 'Crypto')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id}"
    
    
class TradeRequest(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trade_requests")
    trader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_trades")
    offered_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offered_trades")
    requested_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="requested_trades")
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} offers {self.offered_product.name} for {self.requested_product.name}"
    
    
