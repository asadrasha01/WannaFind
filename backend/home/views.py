from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from .forms import UserLoginForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm, ItemRequestForm, UserRegistrationForm
from .models import ItemRequest, Message
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q

# Create your views here.
def homepage(request):
    return render(request, 'home/homepage.html')

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Set user as inactive until confirmed
            user.save()

        """  # Send confirmation email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('home/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Please confirm your email to complete registration.')
            return redirect('login')"""
    else:
        form = UserCreationForm()
    
    return render(request, 'home/register.html', {'form': form})

# Registration API view
@api_view(['POST'])
def api_register(request):
    form = UserRegistrationForm(data=request.data)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False  # Deactivate until email confirmation
        user.save()

        # Send confirmation email
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('home/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

        return Response({'message': 'Please confirm your email to complete registration.'}, status=status.HTTP_201_CREATED)
    
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

#Login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # Remove the 'request' parameter
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')  # Redirect to a homepage or dashboard
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'home/login.html', {'form': form})
# Login API view
@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#Logout
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'home/profile.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after changing password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'password_changes/change_password.html', {'form': form})

@login_required
def submit_item_request(request):
    if request.method == 'POST':
        form = ItemRequestForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            item_request = form.save(commit=False)
            item_request.user = request.user  # Associate the request with the logged-in user
            item_request.save()
            return redirect('item_requests_list')  # Redirect to the list of item requests
    else:
        form = ItemRequestForm()

    return render(request, 'item_requests/submit_item_request.html', {'form': form})


def request_list_view(request):
    """
    View to render a template with a list of requests.
    """
    requests = ItemRequest.objects.all()
    return render(request, 'item_requests/item_requests_list.html', {'requests': requests})

@login_required
def item_requests_list(request):
    item_requests = ItemRequest.objects.filter(user=request.user)  # Retrieve only the user's requests
    return render(request, 'item_requests/item_requests_list.html', {'item_requests': item_requests})

def item_list(request):
    items = ItemRequest.objects.all()  # Retrieve all items
    return render(request, 'item/item_list.html', {'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(ItemRequest, id=item_id)
    return JsonResponse({
        'title': item.title,
        'description': item.description,
        'image_url': item.image.url,
        'owner': item.user.username,
        'created_at': item.created_at
    })

# Send Message (Chat)
@csrf_exempt
@login_required
def send_message_request(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ItemRequest, id=item_id)
        receiver = item.user
        sender = request.user

        # Parse JSON body to extract content
        data = json.loads(request.body.decode('utf-8'))
        content = data.get('content')  # Retrieve content as plain text

        if content:
            Message.objects.create(
                sender=sender,
                receiver=receiver,
                item=item,
                content=content,  # Save as plain text
                timestamp=timezone.now()
            )
            return JsonResponse({'status': 'success', 'message': 'Message sent successfully.'})

        return JsonResponse({'status': 'error', 'message': 'Message content is required.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


# Accept a message request (item owner only)
@login_required
def accept_message_request(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_accepted = True
    message.is_read = True
    message.save()
    # Redirect to chat_list without additional parameters
    return redirect('chat_detail', item_id=message.item.id, other_user_id=message.sender.id)

@login_required
def reject_message_request(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True  # Mark as read so it doesn’t appear in notifications
    message.save()
    # Optionally, delete or keep for record-keeping
    return redirect('notifications')

# Chat List and Detail Views
@login_required
def chat_list(request):
    # Get all unique conversations for the user
    chats = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        is_accepted=True
    ).values('item', 'sender', 'receiver').distinct()

    chat_list = []
    for chat in chats:
        other_user_id = chat['receiver'] if chat['sender'] == request.user.id else chat['sender']
        other_user = User.objects.get(id=other_user_id)
        item = ItemRequest.objects.get(id=chat['item'])
        
        chat_list.append({
            'other_user': other_user,
            'item': item,
        })

    return render(request, 'chat/chat_list.html', {'chat_list': chat_list})

@login_required
def chat_detail_view(request, item_id, other_user_id):
    item = get_object_or_404(ItemRequest, id=item_id)
    other_user = get_object_or_404(User, id=other_user_id)
    messages = Message.objects.filter(
        item=item,
        is_accepted=True,
        sender__in=[request.user.id, other_user_id],
        receiver__in=[request.user.id, other_user_id]
    ).order_by('timestamp')

    return render(request, 'chat/chat_detail.html', {
        'messages': messages,
        'item': item,
        'other_user': other_user,
    })

# Notifications
@login_required
def notifications(request):
    # Fetch unread message requests for the logged-in user
    message_requests = Message.objects.filter(receiver=request.user, is_read=False, is_accepted=False)

    return render(request, 'notification/notifications.html', {
        'message_requests': message_requests
    })
