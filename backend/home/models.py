from django.db import models
from django.contrib.auth.models import User
import os
import uuid

# Function to generate the directory path for image uploads
def request_directory_path(instance, filename):
    if not instance.id:
        # Generate a temporary path if instance.id is not yet available
        return f"requests/temp/{uuid.uuid4()}_{filename}"
    return f"requests/{instance.id}/{uuid.uuid4()}_{filename}"

class ItemRequest(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home'),
        ('books', 'Books'),
        ('sports', 'Sports'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=request_directory_path, blank=True, null=True, max_length=255)  # Increased max_length
    brand = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=10, choices=[('new', 'New'), ('used', 'Used')])
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if this is a new instance
        super().save(*args, **kwargs)  # Save the instance to generate the ID if new

        if is_new and self.image:
            try:
                # Define paths
                old_path = self.image.path
                filename = f"{uuid.uuid4()}_{os.path.basename(self.image.name)}"
                new_dir = os.path.join('media', 'requests', str(self.id))
                new_path = os.path.join(new_dir, filename)

                # Debug prints
                print("=== DEBUG: Save Method ===")
                print("Old Path:", old_path)
                print("New Directory:", new_dir)
                print("New Path:", new_path)

                # Ensure the new directory exists
                os.makedirs(new_dir, exist_ok=True)

                # Move the file
                os.rename(old_path, new_path)

                # Update the image field to the new path
                self.image.name = os.path.join('requests', str(self.id), filename)

                # Save the instance again to update the image field in the database
                super().save(update_fields=['image'])
            except Exception as e:
                # Log the error for debugging
                print("Error moving image file:", e)
                raise



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
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

