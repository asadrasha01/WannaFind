from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ItemRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_requests')
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='requests/')
    brand = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'