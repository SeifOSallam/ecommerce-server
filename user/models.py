from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    profile_image = models.CharField(max_length=50, null=True, blank=True)
    cover_image = models.CharField(max_length=50, null=True, blank=True)
