from django.db import models
from user.models import User
# Create your models here.

class SavedAddresses(models.Model):
    address_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    landline_number = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)
    additional_desc = models.CharField(max_length=50)

    user = models.ForeignKey(User, on_delete=models.CASCADE)