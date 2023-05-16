from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    """Admin interface config for users"""

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active'
    ]