from django import forms

from . import models


class StoreForm(forms.ModelForm):
    class Meta:
        model = models.Store
        fields = '__all__'


class BusinessHourForm(forms.ModelForm):
    class Meta:
        model = models.BusinessHour
        exclude = ('store_object',)


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        exclude = ('store_object',)


class ManagerForm(forms.ModelForm):
    class Meta:
        model = models.Manager
        exclude = ('store_object',)
