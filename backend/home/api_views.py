from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.urls import reverse


@api_view(['POST'])
@permission_classes([AllowAny])  # This ensures anyone can access the register endpoint
def api_register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save(commit=False)  # Save the user 
        user.is_active = False  
        user.save()

        # Send activation email
        send_activation_email(user, request)
        return Response({'message': 'Registration successful. Please confirm your email to activate your account.'}, status=201)
    else:
        return Response(serializer.errors, status=400)


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

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    subject = "Activate Your Account"
    message = f"Hi {user.username},\n\nThank you for registering. Click the link below to activate your account:\n\n{activation_link}\n\nBest regards,\nThe Team"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response({'error': 'Please provide both current and new passwords.'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    # Refresh the token
    Token.objects.filter(user=user).delete()
    new_token = Token.objects.create(user=user)

    return Response({
        'message': 'Password changed successfully.',
        'token': new_token.key  # Return new token if old tokens are invalidated
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
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
