from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from .models import Profile, ItemRequest

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address', 'class': 'form-control'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is no user registered with this email address.")
        return email

class SetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label="New Password"
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone_number', 'profile_image']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2'] 

class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['item_name', 'description', 'category', 'image', 'brand']  # No need to include 'id'

    def __init__(self, *args, **kwargs):
        super(ItemRequestForm, self).__init__(*args, **kwargs)
        # Set 'id' as read-only if you include it
        self.fields['id'] = forms.CharField(initial=self.instance.id if self.instance else None, disabled=True)
