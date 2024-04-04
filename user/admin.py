from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "is_staff", "is_verified"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("profile_image", "cover_image", "is_verified")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "classes": ("wide"),
            "fields": ("username", "email", "profile_image", "cover_image", "is_verified"),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["profile_image"].required = False
        form.base_fields["cover_image"].required = False
        return form


admin.site.register(User, CustomUserAdmin)
