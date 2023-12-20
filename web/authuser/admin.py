from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', )  # Add 'id' to display


# Register the User model with the custom admin class
admin.site.register(User, UserAdmin)
