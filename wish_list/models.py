from django.db import models
from user.models import User
from products.models import Product

# Create your models here.

class WishList(models.Model):
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)

    