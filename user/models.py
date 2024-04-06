from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from rest_framework import permissions


class User(AbstractUser):
    profile_image = CloudinaryField('profile_image', null=True)
    cover_image = CloudinaryField('cover_image', null=True)
    is_verified = models.BooleanField(default=False)
    

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return request.user.is_staff
        return request.method in permissions.SAFE_METHODS
