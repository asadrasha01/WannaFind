from django.urls import path
from . import api_views

urlpatterns = [
    
    # Authentication endpoints
    path('register/', api_views.api_register, name='api_register'),
    path('login/', api_views.api_login, name='api_login'),
    path('logout/', api_views.api_logout, name='api_logout'),
    
    # Profile endpoint
    path('profile/', api_views.profile_view, name='api_profile'),
    # Activation and password change endpoints
    path('activate/<uidb64>/<token>/', api_views.activate_account, name='activate_account'),
    path('change_password/', api_views.change_password, name='change_password'),
]
