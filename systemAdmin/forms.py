from django import forms
from django.contrib.auth import forms as auth_form
from .models import SystemAdmin
from django.core.exceptions import ValidationError


# ADMIN LOGINUP FORM
class AdminLoginForm(auth_form.AuthenticationForm):
    username = auth_form.UsernameField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'type': 'text',
                'name': 'username',
                'id': 'user_name',
                'class': 'form-control',
                'placeholder': 'Enter User Name',
            }
        ),
    )
    password = forms.CharField(
        # label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'name': 'password',
                'id': 'password',
                'class': 'form-control',
                'placeholder': 'Password',
            }
        ),
    )


# ADMIN SIGNUP FORM
class AdminSignUpForm(auth_form.UserCreationForm):
    username = auth_form.UsernameField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'type': 'text',
                'name': 'username',
                'id': 'user_name',
                'class': 'form-control',
                'placeholder': 'Enter User Name',
            }
        ),
    )

    email = forms.EmailField(
        max_length=500,
        widget=forms.EmailInput(
            attrs={
                'type': 'email',
                'name': 'email',
                'id': 'admin_email',
                'placeholder': 'Email Address i.e. admin@orims.com',
                'class': 'form-control',
            }
        ),

    )

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'name': 'password1',
                'id': 'admin_password1',
                'class': 'form-control',
                'placeholder': 'Enter Admin Password',
            }
        ),

    )

    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'name': 'password2',
                'id': 'admin_password2',
                'class': 'form-control',
                'placeholder': 'Re-Enter Password',
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = SystemAdmin.objects.filter(system_admin_user_name=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = SystemAdmin.objects.filter(system_admin_email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = SystemAdmin.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
