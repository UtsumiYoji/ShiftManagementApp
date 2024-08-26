from django.contrib.auth import forms as auth_forms
from django import forms

from . import models


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = (
            'email', 'first_name', 'last_name', 'password1', 'password2',
        )


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta:
        model = models.User
        fields = (
            'email', 'first_name', 'last_name', 'phone_number'
        )
        exclude = ('password', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')


class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        exclude = ('user_object', )


class BankInformationForm(forms.ModelForm):
    class Meta:
        model = models.BankInformation
        exclude = ('user_object', )


class UserLeftForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('date_left', )


class EmployeeInformationForm(forms.ModelForm):
    class Meta:
        model = models.EmployeeInformation
        exclude = ('user_object', )


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        exclude = ('user_object', )


class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        exclude = ('user_object', )
