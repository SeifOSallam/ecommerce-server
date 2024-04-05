from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from cart.models import Cart
from saved_addresses.models import SavedAddresses
from user.models import User
from products.models import Product
# Create your models here.


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=12, decimal_places=3)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_address = models.ForeignKey(SavedAddresses, on_delete=models.RESTRICT)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    class Meta():
        unique_together = (('order', 'product'))
