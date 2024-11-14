from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
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
from .forms import UserLoginForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm, ItemRequestForm, UserRegistrationForm, PasswordResetForm, SetPasswordForm
from .models import ItemRequest, Message
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q, F
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def homepage(request):
    return render(request, 'home/homepage.html')

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set as inactive until confirmed
            user.save()

            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construct activation link
            activation_link = f"{request.scheme}://{request.get_host()}/activate/{uid}/{token}/"
            
            # Send email with the activation link
            send_mail(
                subject="Activate Your Account",
                message=f"Thank you for registering. Click the link below to activate your account:\n\n{activation_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return render(request, 'registration/success.html', {'message': 'Please confirm your email to complete registration.'})
    else:
        form = UserRegistrationForm()
    
    return render(request, 'home/register.html', {'form': form})

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

User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('home')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_user = User.objects.filter(email=email).first()
            if associated_user:
                subject = "Password Reset Requested"
                
                # Generate the token and UID
                token = default_token_generator.make_token(associated_user)
                uid = urlsafe_base64_encode(force_bytes(associated_user.pk))

                # Construct the reset link
                reset_link = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )

                # Send the email with reset link
                message = render_to_string('home/password_reset_email.html', {
                    'reset_link': reset_link,
                    'user': associated_user,
                })
                send_mail(subject, message, settings.EMAIL_HOST_USER, [associated_user.email])
                messages.success(request, "An email has been sent to reset your password.")
                return redirect("password_reset_done")
    else:
        password_reset_form = PasswordResetForm()

    return render(request, "home/password_reset_form.html", {"password_reset_form": password_reset_form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
    else:
        messages.error(request, 'The password reset link is invalid, possibly because it has already been used.')
        return redirect('password_reset')

    return render(request, 'home/password_reset_confirm.html', {'form': form})

@login_required
def change_password_in_profile(request):
    # This is used by logged-in users to change their password in the profile.
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after changing password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'home/change_password.html', {'form': form})

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
        receiver_id = request.POST.get('receiver_id')
        receiver = item.user if item.user != request.user else get_object_or_404(User, id=receiver_id)
        sender = request.user

        # Parse JSON body to extract content
        data = json.loads(request.body.decode('utf-8'))
        content = data.get('content')  # Retrieve content as plain text

        if content:
            # Save to database
            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                item=item,
                content=content,
                timestamp=timezone.now()
            )

            # Confirm the save in logs
            print("Message saved:", message)

            # Broadcast message over WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{item_id}_{receiver.id}',  # Define room name format based on item and user ID
                {
                    'type': 'chat_message',
                    'message': content,
                    'sender': sender.username,
                    'timestamp': message.timestamp.strftime('%H:%M, %b %d')
                }
            )

            return JsonResponse({'status': 'success', 'content': content})
        return JsonResponse({'status': 'error', 'message': 'Message content is required.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



# Accept a message request (item owner only)
@login_required
def accept_message_request(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_accepted = True
    message.is_read = True
    message.save()

    # Notify other user via WebSocket that the request was accepted
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{message.item.id}_{message.sender.id}',  # room_name format
        {
            'type': 'chat_message',
            'message': 'Your request was accepted!',
            'sender': request.user.username,
            'timestamp': timezone.now().strftime('%H:%M, %b %d')
        }
    )

    # Remove from notifications
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
    # Get distinct chats by grouping by each unique item and user pair
    chats = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        ~Q(sender=request.user, receiver=request.user),  # Exclude self-chats
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
    
    # Retrieve messages from the database for this chat
    messages = Message.objects.filter(
        item=item,
        sender__in=[request.user.id, other_user_id],
        receiver__in=[request.user.id, other_user_id]
    ).order_by('timestamp')
    
    # Optional: Debug log to verify messages retrieved
    print("Retrieved messages for chat:", messages)

    return render(request, 'chat/chat_detail.html', {
        'messages': messages,
        'item': item,
        'other_user': other_user,
    })

@login_required
def get_chat_messages(request, item_id, other_user_id):
    item = get_object_or_404(ItemRequest, id=item_id)
    other_user = get_object_or_404(User, id=other_user_id)
    
    # Retrieve all messages between the two users for this item
    messages = Message.objects.filter(
        item=item,
        sender__in=[request.user.id, other_user_id],
        receiver__in=[request.user.id, other_user_id]
    ).order_by('timestamp')
    
    # Debugging: Print messages retrieved
    print("Retrieved messages for chat:", messages)

    return render(request, 'chat/chat_detail.html', {
        'messages': messages,
        'item': item,
        'other_user': other_user
    })

# Notifications
@login_required
def notifications(request):
    # Fetch unread message requests for the logged-in user
    message_requests = Message.objects.filter(receiver=request.user, is_read=False, is_accepted=False)

    return render(request, 'notification/notifications.html', {
        'message_requests': message_requests
    })
