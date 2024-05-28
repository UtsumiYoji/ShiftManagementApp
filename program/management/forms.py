from django import forms

from . import models
from user import models as user_models


class UserAccessAuthorizationsForm(forms.ModelForm):
    class Meta:
        model = models.UserAccessAuthorizations
        fields = '__all__'


class EmployeeTypeAccessAuthorizationsForm(forms.ModelForm):
    class Meta:
        model = models.EmployeeTypeAccessAuthorizations
        fields = '__all__'


class EmployeeInformationForm(forms.ModelForm):
    class Meta:
        model = user_models.EmployeeInformations
        fields = (
            'user_object',
            'wage',
            'wage_is_based_on',
            'employee_type_object'
            )