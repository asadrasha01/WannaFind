from django.urls import path
from . import api_views

urlpatterns = [
    
    # Authentication endpoints
    path('register/', api_views.api_register, name='api_register'),
    path('login/', api_views.api_login, name='api_login'),
    path('logout/', api_views.api_logout, name='api_logout'),
    
    # Profile endpoint
    path('profile/', api_views.profile_view, name='api_profile'),
    path('check-username/', api_views.check_username, name='check-username'),
    path('check-email/', api_views.check_email, name='check-email'),
    # Activation and password change endpoints
    path('activate/<uidb64>/<token>/', api_views.activate_account, name='activate_account'),
    
    path('password-reset/', api_views.api_password_reset_request, name='api_password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', api_views.api_password_reset_confirm, name='password_reset_confirm'),
    # Change password in profile
    path('change-password/', api_views.api_change_password, name='api_change_password'),
    #
    path('submit-item/', api_views.submit_item, name='submit_item'),
    path('item-request-detail/<int:item_id>/', api_views.item_request_detail, name='item_request_detail'),
    path('item-list/', api_views.item_list, name='item_list'),
    path('my-requests/', api_views.my_requests, name='my_requests'),
    path('toggle-item-status/<int:item_id>/', api_views.toggle_item_status, name='toggle_item_status'),
    path('delete-request/<int:pk>/', api_views.delete_request, name='delete-request'),
    path('send-message/<int:item_id>/', api_views.send_message_request, name='send_message_request'),
    path('notifications/', api_views.get_notifications, name='get_notifications'),
    path('notifications/accept/<int:message_id>/', api_views.accept_notification, name='accept_notification'),
    path('notifications/reject/<int:message_id>/', api_views.reject_notification, name='reject_notification'),
    path('chat-list/', api_views.chat_list, name='chat_list'),
    path('chat-messages/<int:item_id>/<int:other_user_id>/', api_views.get_chat_messages, name='get_chat_messages'),
    path('send-chat-message/', api_views.send_chat_message, name='send_chat_message'),




    
]
