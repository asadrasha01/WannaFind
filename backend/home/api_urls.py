from django.urls import path
from . import api_views

urlpatterns = [
    
    # Authentication endpoints
    path('register/', api_views.api_register, name='api_register'),
    path('login/', api_views.api_login, name='api_login'),
    path('logout/', api_views.api_logout, name='api_logout'),
    
    # Profile endpoint
    path('profile/', api_views.profile_view, name='api_profile'),
    path('check-username/', api_views.check_username),
    path('check-email/', api_views.check_email),
    # Activation and password change endpoints
    path('activate/<uidb64>/<token>/', api_views.activate_account, name='activate_account'),
    
    path('password-reset/', api_views.api_password_reset_request, name='api_password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', api_views.api_password_reset_confirm, name='password_reset_confirm'),
    # Change password in profile
    path('api/change-password/', api_views.api_change_password, name='api_change_password'),
    
]
