from django import forms
from django.contrib.auth import forms as auth_form
from .models import SystemAdmin
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password


# START : ADMIN LOGIN FORM
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

# End of : class AdminLoginForm():


# START : ADMIN SIGNUP FORM
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

    agree = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'type': 'checkbox',
                'name': 'agree',
                'id': 'admin_agree',
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = SystemAdmin.objects.filter(system_admin_user_name=username)
        if r.count():
            raise ValidationError("Username already exists. Please Choose a different Username and Try again.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = SystemAdmin.objects.filter(system_admin_email=email)
        if r.count():
            raise ValidationError("Email already exists. Please Choose a different email address and Try again.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match. Please ensure that both passwords entered are exactly the\
             same.")

        return password2

    def confirm_agreement(self):
        agree = self.cleaned_data.get('agree')
        if not agree:
            raise ValidationError("You must first agree to our terms of use, Policies and conditions.\
            Check or tick in the box provided on the field below(at the right), to confirm your agreement.")
        return agree

    def save(self, commit=True):
        user = SystemAdmin(
            system_admin_user_name = self.cleaned_data['username'],
            system_admin_email = self.cleaned_data['email'],
             system_admin_password = make_password(self.cleaned_data['password1'])
        )

        user.save()
        # print(check_password(self.cleaned_data['password1'], user.system_admin_password))
        return user
# End of : class AdminSignUpForm():
