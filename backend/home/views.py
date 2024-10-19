from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from .forms import UserLoginForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm, ItemRequestForm
from .models import ItemRequest


# Create your views here.
def homepage(request):
    return render(request, 'home/homepage.html')

#Registration 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until confirmed
            user.save()

            # Send confirmation email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('home/accaunt_activationemail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Please confirm your email to complete registration.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
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
                return redirect(homepage)  # Redirect to a homepage or dashboard
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
