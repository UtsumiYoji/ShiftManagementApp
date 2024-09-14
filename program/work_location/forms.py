from django import forms

from . import models


class WorkLocationForm(forms.ModelForm):
    class Meta:
        model = models.WorkLocation
        exclude = ('made_on',)
