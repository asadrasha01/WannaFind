from .serializers import UserRegistrationSerializer, UserProfileSerializer, ItemRequestSerializer, MessageSerializer
from .models import ItemRequest, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Q, Max
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError


@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    try:
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            send_activation_email(user, request)
            return Response({'message': 'Registration successful. Please confirm your email to activate your account.'}, status=201)
        else:
            return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])  # Ensures login is open to unauthenticated users
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Ensure the user is active
        if user.is_active:
            # Generate or retrieve the token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Account is inactive.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_logout(request):
    if request.user.is_authenticated:
        request.user.auth_token.delete()  # Remove token
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Not logged in"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Activation link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)

def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"{request.scheme}://{get_current_site(request).domain}/api/activate/{uid}/{token}/"
    login_link = f"{request.scheme}://{get_current_site(request).domain}/login/"
    subject = "Activate Your Account"
    message = (
        f"Hi {user.username},\n\n"
        f"Click the link below to activate your account:\n\n{activation_link}\n\n"
        f"After activating, you can login here:\n\n{login_link}\n\n"
        "Best regards,\nThe Team"
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to initiate a password reset
def api_password_reset_request(request):
    email = request.data.get('email')
    if email:
        associated_user = User.objects.filter(email=email).first()
        if associated_user:
            subject = "Password Reset Requested"
            
            # Generate the token and UID
            token = default_token_generator.make_token(associated_user)
            uid = urlsafe_base64_encode(force_bytes(associated_user.pk))

            # Generate the reset link using reverse to match the correct pattern
            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            # Render the email content
            message = f"Hi {associated_user.username},\n\nClick the link below to reset your password:\n\n{reset_link}\n\nBest regards,\nWannaFind"

            # Send the reset email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [associated_user.email])

            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to reset password using a valid link
def api_password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

    if default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "The reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only logged-in users can access this
def api_change_password(request):
    # Get the logged-in user
    user = request.user
    
    # Validate the request body
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not current_password or not new_password:
        return Response({'error': 'Both current and new passwords are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the password
    user.set_password(new_password)
    user.save()

    # Update session authentication hash to prevent logout after password change
    update_session_auth_hash(request, user)

    # Optionally refresh the user's token (if using token-based authentication)
    Token.objects.filter(user=user).delete()
    new_token = Token.objects.create(user=user)

    return Response({
        'message': 'Password has been changed successfully.',
        'token': new_token.key  # Return the new token for API authentication
    }, status=status.HTTP_200_OK)    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    
    if request.method == 'GET':
        # Return the current user's profile data
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Allow updating username, email, or other fields
        data = request.data
        if 'username' in data:
            if User.objects.filter(username=data['username']).exclude(id=user.id).exists():
                return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'email' in data:
            if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
                return Response({'error': 'Email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# Check Username Availability
@api_view(['POST'])
@permission_classes([AllowAny])  # Explicitly allow unauthenticated access
def check_username(request):
    username = request.data.get('username')
    if username and User.objects.filter(username=username).exists():
        return Response({'available': False}, status=status.HTTP_200_OK)
    return Response({'available': True}, status=status.HTTP_200_OK)

# Check Email Availability
@api_view(['POST'])
@permission_classes([AllowAny])  # Explicitly allow unauthenticated access
def check_email(request):
    email = request.data.get('email')
    if email and User.objects.filter(email=email).exists():
        return Response({'available': False}, status=status.HTTP_200_OK)
    return Response({'available': True}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_item(request):
    data = request.data.copy()
    data['user'] = request.user.id  # Automatically associate the user

    if 'image' in request.FILES:
        data['image'] = request.FILES['image']

    serializer = ItemRequestSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        try:
            item = serializer.save()
            return Response(
                {
                    'message': 'Item submitted successfully.',
                    'item': {
                        'id': item.id,
                        'title': item.title,
                        'description': item.description,
                        'image': item.image.url if item.image else None,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print("Error saving item:", str(e))
            return Response({'error': 'Error saving item.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("Validation errors:", serializer.errors)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_request_detail(request, item_id):

    try:
        item_request = ItemRequest.objects.get(id=item_id, user=request.user)
    except ItemRequest.DoesNotExist:
        return Response({'error': 'Item request not found or unauthorized.'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the fetched item request
    serializer = ItemRequestSerializer(item_request)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_requests(request):
    item_requests = ItemRequest.objects.filter(user=request.user)
    serializer = ItemRequestSerializer(item_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_item_status(request, item_id):
    try:
        item = ItemRequest.objects.get(id=item_id, user=request.user)
        item.active = not item.active
        item.save()
        return Response({'message': 'Status toggled successfully.'}, status=status.HTTP_200_OK)
    except ItemRequest.DoesNotExist:
        return Response({'error': 'Item not found or not authorized.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_request(request, pk):  # Change item_id to pk
    try:
        item = ItemRequest.objects.get(id=pk, user=request.user)
        item.delete()
        return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_200_OK)
    except ItemRequest.DoesNotExist:
        return Response({'error': 'Item not found or not authorized.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list(request):
    try:
        # Exclude the user's own items
        items = ItemRequest.objects.exclude(user=request.user)
        serializer = ItemRequestSerializer(items, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        print("Error in item_list:", str(e))
        return Response({'error': 'Server error occurred.'}, status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_request(request, item_id):
    item = get_object_or_404(ItemRequest, id=item_id)
    content = request.data.get('content')
    receiver_id = request.data.get('receiver_id')

    if not content:
        return Response({'error': 'Message content is required.'}, status=400)

    if item.user == request.user:
        if not receiver_id:
            return Response({'error': 'Receiver ID is required for self-posted items.'}, status=400)
        receiver = get_object_or_404(User, id=receiver_id)
    else:
        receiver = item.user

    message_data = {
        'sender': request.user.id,
        'receiver': receiver.id,
        'item': item.id,
        'content': content,
    }

    serializer = MessageSerializer(data=message_data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'message': 'Message sent successfully.'}, status=201)
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    user = request.user
    # Fetch all unread messages for the logged-in user
    messages = Message.objects.filter(receiver=user, is_read=False).order_by('-timestamp')

    # Serialize the messages
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_notification(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_accepted = True
    message.is_read = True
    message.save()
    return Response({'status': 'success', 'message': 'Notification accepted.'}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_notification(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.delete()
    return Response({'status': 'success', 'message': 'Notification rejected.'}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list(request):
    user = request.user
    chats = (
        Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        )
        .distinct('item', 'sender', 'receiver')
    )

    chat_data = []
    for chat in chats:
        other_user = chat.receiver if chat.sender == user else chat.sender
        item = chat.item
        chat_data.append({
            'userId': other_user.id,
            'username': other_user.username,
            'itemId': item.id,
            'itemTitle': item.title,
            'latestMessage': chat.content,
            'timestamp': chat.timestamp,
        })

    return Response(chat_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_messages(request, item_id, other_user_id):
    user = request.user
    item = get_object_or_404(ItemRequest, id=item_id)
    other_user = get_object_or_404(User, id=other_user_id)

    messages = Message.objects.filter(
        item=item,
        sender__in=[user, other_user],
        receiver__in=[user, other_user]
    ).order_by('timestamp')

    serialized_messages = [
        {
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'content': message.content,
            'timestamp': message.timestamp,
        }
        for message in messages
    ]

    return Response(serialized_messages)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_chat_message(request):
    sender = request.user
    receiver_id = request.data.get('receiver_id')
    content = request.data.get('content')
    item_id = request.data.get('item_id')

    if not content:
        return Response({'error': 'Message content is required.'}, status=400)

    if not receiver_id:
        return Response({'error': 'Receiver ID is required.'}, status=400)

    if not item_id:
        return Response({'error': 'Item ID is required.'}, status=400)

    receiver = get_object_or_404(User, id=receiver_id)
    item = get_object_or_404(ItemRequest, id=item_id)

    message = Message.objects.create(sender=sender, receiver=receiver, item=item, content=content)

    return Response({
        'id': message.id,
        'sender': sender.username,
        'receiver': receiver.username,
        'content': message.content,
        'timestamp': message.timestamp,
    }, status=201)


