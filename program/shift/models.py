from django.db import models
from colorfield.fields import ColorField

from user import models as user_models
from work_location.models import WorkLocation

# Create your models here.
class WorkLocation(models.Model):
    work_location_object = models.ForeignKey(WorkLocation, verbose_name='copy_from', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=False, blank=False)
    start_at = models.TimeField(null=False, blank=False)
    finish_at = models.TimeField(null=False, blank=False)
    estimated_sales = models.PositiveSmallIntegerField(null=True, blank=True)

    # Work location info which could be coped from other models
    name = models.CharField(max_length=255, blank=False, null=False)
    place_name = models.CharField(max_length=255, blank=True, null=True, help_text='If your store is inside of mall or something')
    address1 = models.CharField('adress1', help_text='Street name', max_length=255, null=True, blank=True)
    address2 = models.CharField('adress2', help_text='(Optional) building name', max_length=255, null=True, blank=True)
    city = models.CharField('city', help_text='or Town', max_length=255, null=True, blank=True)
    postal_code = models.CharField('postal code', max_length=255, null=True, blank=True)
    province = models.CharField('province', max_length=255, null=True, blank=True)
    color = ColorField(null=False, blank=False, help_text='Color for this location in calendar')

class UserShift(models.Model):
    user_object = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, null=True, blank=True)
    start_at = models.DateTimeField(null=False, blank=False)
    finish_at = models.DateTimeField(null=False, blank=False)
    note = models.CharField(max_length=100, null=True, blank=True)

class BreakTime(models.Model):
    user_shift_object = models.ForeignKey(UserShift, on_delete=models.CASCADE, null=False, blank=False)
    start_at = models.DateTimeField(null=False, blank=False)
    finish_at = models.DateTimeField(null=False, blank=False)