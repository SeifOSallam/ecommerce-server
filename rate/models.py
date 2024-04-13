from django.db import models
from user.models import User
from products.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Rate(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rate = models.PositiveIntegerField(validators = [MaxValueValidator(5)])

    class Meta():
        unique_together = (('user', 'product'))