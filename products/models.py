from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    representative = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"