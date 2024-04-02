from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class User(AbstractUser):
    profile_image = CloudinaryField('profile_image', null=True)
    cover_image = CloudinaryField('cover_image', null=True)
