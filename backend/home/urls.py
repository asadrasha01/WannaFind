from django.urls import path
from .api_views import RequestListView, RequestDetailView
from django.contrib.auth import views as auth_views
from .views import register, user_login, logout_view, activate, profile, change_password, request_list_view, submit_item_request
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name ='homapage'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('change_password/', change_password, name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='home/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('api/requests/', RequestListView.as_view(), name='request-list'),
    path('api/requests/<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
    path('requests/', request_list_view, name='request-list-html'),
    path('submit-request/', submit_item_request, name='submit_item_request'),
    path('item-requests/', views.item_requests_list, name='item_requests_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)