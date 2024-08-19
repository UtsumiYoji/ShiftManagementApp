from django import forms

from . import models


class WorkLocationForm(forms.ModelForm):
    class Meta:
        model = models.WorkLocation
        fields = '__all__'


class BusinessHourForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_fields['day'].disabled = True

    class Meta:
        model = models.BusinessHour
        exclude = ('work_location_object',)
