from django import forms
from django.urls import resolve

from urllib.parse import urlparse

from . import models
from user import models as user_models


class CustomURLField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = forms.URLInput()
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        return value


class UserAccessAuthorizationsForm(forms.ModelForm):
    class Meta:
        model = models.UserAccessAuthorization
        fields = '__all__'


class EmployeeTypeAccessAuthorizationsForm(forms.ModelForm):
    class Meta:
        model = models.EmployeeTypeAccessAuthorization
        fields = '__all__'


class EmployeeInformationForm(forms.ModelForm):
    class Meta:
        model = user_models.EmployeeInformation
        fields = (
            'user_object',
            'wage',
            'wage_is_based_on',
            'employee_type_object'
            )