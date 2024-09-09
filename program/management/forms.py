from django import forms

from . import models
from user import models as user_models


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
            'wage',
            'wage_is_based_on',
            'employee_type_object'
            )
        

class UserLeftForm(forms.ModelForm):
    class Meta:
        model = user_models.User
        fields = ('date_left', )


class EmployeeInformationForm(forms.ModelForm):
    class Meta:
        model = user_models.EmployeeInformation
        exclude = ('user_object', )


class ImageForm(forms.ModelForm):
    class Meta:
        model = user_models.Image
        exclude = ('user_object', )


class NoteForm(forms.ModelForm):
    class Meta:
        model = user_models.Note
        fields = ('title', 'note')


class DateLeftForm(forms.ModelForm):
    class Meta:
        model = user_models.User
        fields = ('date_left', )