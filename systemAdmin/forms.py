from django import forms
from django.contrib.auth import forms as auth_form


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
                'placeholder': 'User Name',
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
