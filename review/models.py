from django.db import models
from user.models import User
from products.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def _str_(self):
        return f"Review by {self.user.username} for {self.product.name}"