from django import forms

from . import models


class WorkLocationForm(forms.ModelForm):
    class Meta:
        model = models.WorkLocation
        fields = '__all__'


class BusinessHourForm(forms.ModelForm):
    class Meta:
        model = models.BusinessHour
        exclude = ('work_location_object',)
