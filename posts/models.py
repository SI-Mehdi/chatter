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

    # Many to many as we have a user to user relation, 'self' means relation to current model (table)
    # symmetrical is false because if a user follows someone, other user doesn't have to follow them
    # related_name is used to access the reverse relationship, so the users this one follows
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def toggle_follow(self, to_follow):
        if self == to_follow:
            return # Cannot follow self
        if self in to_follow.followers.all(): # If current user is in the followers of target user, then we remove (unfollow) from the followers
            to_follow.followers.remove(self)
        else:
            to_follow.followers.add(self) # Add current user to target user's followers


    def is_following(self, user):
        return user in self.following.all() # Check if target user is in the following list of current user

    def follower_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length= 150, blank=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    # The 'upload_to' folder must be in the 'media' folder of the project root, project root is where manage.py is
    body = models.CharField(max_length=500, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)