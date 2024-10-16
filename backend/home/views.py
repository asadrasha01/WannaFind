from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') #Redirect to home page
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'home/login.html')

#Logout
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'home/profile.html', {'user': request.user})

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