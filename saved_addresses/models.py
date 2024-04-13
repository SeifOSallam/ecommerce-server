from django.db import models

from user.models import User


class SavedAddresses(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)
    desc = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
