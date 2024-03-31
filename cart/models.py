from django.db import models
from user.models import User
from products.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.RESTRICT)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.RESTRICT)
    product = models.ForeignKey(Product, on_delete = models.RESTRICT)
    quantity = models.PositiveIntegerField(default=1)


    class Meta():
        unique_together = (('cart', 'product'))