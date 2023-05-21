from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    bio = models.CharField(max_length=500, blank=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length= 150, blank=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    # The 'upload_to' folder must be in the 'media' folder of the project root, project root is where manage.py is
    body = models.CharField(max_length=500, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)