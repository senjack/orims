from django import forms
from django.forms import ModelForm
from django.contrib.auth import forms as auth_form
from .models import *
from django.core.exceptions import ValidationError


# START : UNIT CREATION / UPDATE FORM
class UnitCreationForm(ModelForm):

    class Meta:
        model = ServiceUnit
        fields = [#'system_admin_id',
                  'unit_id',
                  'unit_name',
                  'unit_type',
                  'unit_description',

                  'unit_logo',
                  'unit_featured_image',
                  'unit_cover_photo'
                  ]
        widgets = {
            #'system_admin_id': forms.Select(),
            #'unit_id':forms.Select(),
            'unit_name': forms.TextInput(
                attrs={
                    'autofocus': True,
                    'type': 'text',
                    'name': 'unitname',
                    'id': 'unit_name',
                    'class': 'form-control',
                    'placeholder': 'Enter Service Unit Name',
                    'style': 'border-radius:3px;width:100%;',
                }
            ),
            'unit_type': forms.Select(
                attrs={
                        'name': 'unit_category',
                        'id': 'unit_category',
                        'class': 'form-control',
                        'style': 'border-radius:3px;width:100%;',
                    }
            ),
            'unit_description': forms.Textarea(
                attrs={
                    'name': 'unit_description',
                    'id': 'unit_description',
                    'class': 'form-control',
                    'placeholder': 'Enter Service unit description ( Less that 1024 characters )',
                    'style': 'min-height:200px;border-radius:3px;height:100%;',
                }
            ),
            'unit_logo': forms.FileInput(),
            'unit_featured_image': forms.FileInput(),
            'unit_cover_photo': forms.FileInput()
        }


# End of : class AdminSignUpForm():
