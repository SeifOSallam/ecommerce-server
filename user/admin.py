from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("profile_image", "cover_image")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("profile_image", "cover_image")}),
    )


admin.site.register(User, CustomUserAdmin)
