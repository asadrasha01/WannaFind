from django.urls import path
from django.contrib.auth import views as auth_views
from .views import homepage, register, user_login, logout_view, activate, profile, change_password_in_profile, request_list_view, submit_item_request, item_list, chat_list, accept_message_request
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home and Authentication
    path('', homepage, name='homepage'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),

    # Email Activation
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    ## Password change in profile
    path('change-password/', views.change_password_in_profile, name='change_password_in_profile'),
    
    # Password reset request
    path('password-reset/', views.password_reset_request, name='password_reset'),
    
    # Confirmation that the reset email was sent
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'), name='password_reset_done'),
    
    # Link to reset the password using uid and token
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'), name='password_reset_confirm'),
    
    # Confirmation that the password was reset successfully
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name='password_reset_complete'),

    # Item Requests
    path('requests/', request_list_view, name='request-list-html'),
    path('submit-request/', submit_item_request, name='submit_item_request'),
    path('item-requests/', views.item_requests_list, name='item_requests_list'),
    path('items/', item_list, name='item_list'),

    # Notifications and Message Requests
    path('notifications/', views.notifications, name='notifications'),
    path('message/<int:message_id>/accept/', views.accept_message_request, name='accept_message_request'),
    path('message/<int:message_id>/reject/', views.reject_message_request, name='reject_message_request'),

    # Chat
    path('chats/', views.chat_list, name='chat_list'), # Consolidated chat list and detail view
    path('chats/<int:item_id>/<int:other_user_id>/', views.chat_detail_view, name='chat_detail'),
    path('item_request/<int:item_id>/send_message/', views.send_message_request, name='send_message_request'),
    path('message/<int:message_id>/accept/', accept_message_request, name='accept_message_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)