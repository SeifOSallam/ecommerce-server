from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    profile_image = models.CharField(max_length=50, null=True)
    cover_image = models.CharField(max_length=50, null=True)


