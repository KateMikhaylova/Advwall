from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Provides admin functionality for a custom User model.
    """
    fieldsets = (
        (None, {"fields": ("username", "email", "phone_number", "password", "type")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    ("is_staff",
                     "is_superuser"),
                    # "groups",
                ),
            },
        ),
        ("Important dates", {"fields": (("last_login", "date_joined"),)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'phone_number', 'type'),
            },
        ),
    )
    list_display = ('id', "username", "email", "phone_number", "type", "country", "city")
    list_filter = ('type', "is_staff", "is_superuser", "is_active", "country", "city")
    search_fields = ("username", "email", "country", "city")
    readonly_fields = ("last_login", "date_joined")
