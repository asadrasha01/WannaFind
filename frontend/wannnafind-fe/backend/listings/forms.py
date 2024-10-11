from django import forms
from .models import Item

class RequestItemForm(forms.Form):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'image', 'user_contact']