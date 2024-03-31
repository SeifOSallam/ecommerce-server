from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from cart.models import Cart
from user.models import User
from saved_addresses.models import SavedAddresses
# Create your models here.

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=12, decimal_places=3)

    STATUS_CHOICES = {
        "PENDING": 'pending',
        "SHIPPED": 'shipped',
        "DELIVERED": 'delievered',
    }

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    cart = models.ForeignKey(Cart, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    saved_address = models.ForeignKey(SavedAddresses, on_delete=models.RESTRICT)

