from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='items/')
    brand = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)