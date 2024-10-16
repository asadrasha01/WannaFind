from django.urls import path
from .api_views import ItemListView, CustomAPI
from django.contrib.auth import views as auth_views
from .views import register, user_login, logout_view, activate, profile
from . import views

urlpatterns = [
    path('', views.homepage, name ='homapage'),
    path('api/items/', ItemListView.as_view(), name='item-list'),
    path('api/custom/', CustomAPI.as_view(), name='custom-api'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='home/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', profile, name='profile'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

]