from django import forms
from django.forms import ModelForm
from django.contrib.auth import forms as auth_form
from .models import *
from django.core.exceptions import ValidationError


# START : ADMIN SIGNUP FORM
class UnitCreationForm(forms.Form,ModelForm):
    class Meta:
        model = ServiceUnit
        fields = ['system_admin_id','unit_name', 'unit_type', 'unit_description', 'unit_logo','unit_featured_image',
                  'unit_cover_photo'
                  ]
        widgets = {
            'unit_name': forms.TextInput(
                attrs={
                    'autofocus': True,
                    'type': 'text',
                    'name': 'unitname',
                    'id': 'unit_name',
                    'class': 'form-control',
                    'placeholder': 'Enter Unit Name',
                    'style': 'border-radius:5px;',
                    'max-length': 512,
                }
            ),
            'unit_type': forms.Select(
                attrs={
                        'name': 'unit_category',
                        'id': 'unit_category',
                        'class': 'form-control',
                        'style': 'border-radius:5px;height:45px;',
                    }
            ),
            'unit_description': forms.Textarea(
                attrs={
                    'name': 'unit_description',
                    'id': 'unit_description',
                    'class': 'form-control',
                    'placeholder': 'Enter Service unit description',
                    'style': 'min-height:600px;border-radius:3px;height:100%;',
                }
            ),
        }


    def set_admin_id(self, system_admin_id):
        self.fields['system_admin_id'] = system_admin_id

"""
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
"""