from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import item_create, item_list, ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('create/', views.item_create, name='item_create'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # Django's auth URLs
    path('items/', views.item_list, name='item_list'),
    path('api/', include(router.urls)),
]