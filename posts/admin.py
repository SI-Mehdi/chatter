from django.contrib import admin
from .models import User, Post

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    """Admin interface config for users"""

    list_display = [ # Fields to display
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active'
    ]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface config for posts"""

    list_display = [
        'title',
        'author',
        'image',
        'body',
        'posted_at'
    ]
    search_fields = [
        'title',
        'author__username'
    ]
    list_filter = [
        'posted_at'
    ]
