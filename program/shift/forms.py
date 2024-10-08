from django import forms

from . import models


class UserShiftForm(forms.ModelForm):
    class Meta:
        model = models.UserShift
        fields = '__all__'


class BreakTimeForm(forms.ModelForm):
    class Meta:
        model = models.BreakTime
        exclude = ('user_shift_object', )