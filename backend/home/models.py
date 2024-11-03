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

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    item = models.ForeignKey(ItemRequest, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)  # Indicates if the message request is accepted
    is_read = models.BooleanField(default=False)      # Indicates if the message is read (for notifications)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} about {self.item.item_name}"
