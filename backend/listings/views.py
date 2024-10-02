from django.shortcuts import redirect, render
from .forms import RequestItemForm  
from .models import Item
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import ItemSerializer
# Create your views here.

from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def item_create(request):
    if request.method == 'POST':
        form = Item(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user  # Associate with logged-in user
            item.save()
            return redirect('item_list')  # Redirect to the item list page after saving
    else:
        form = Item()
    
    return render(request, 'item_form.html', {'form': form})

# listings/views.py
@login_required
def item_list(request):
    items = Item.objects.filter(user=request.user)  # Filter items by the logged-in user
    return render(request, 'item_list.html', {'items': items})

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer