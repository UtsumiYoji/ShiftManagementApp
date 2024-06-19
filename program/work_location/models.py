from django.db import models
from colorfield.fields import ColorField

from user.models import User

# Create your models here.
class WorkLocation(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    place_name = models.CharField(max_length=255, blank=True, null=True, help_text='If your store is inside of mall or something')
    address1 = models.CharField('adress1', help_text='Street name', max_length=255, null=True, blank=True)
    address2 = models.CharField('adress2', help_text='(Optional) building name', max_length=255, null=True, blank=True)
    city = models.CharField('city', help_text='or Town', max_length=255, null=True, blank=True)
    postal_code = models.CharField('postal code', max_length=255, null=True, blank=True)
    province = models.CharField('province', max_length=255, null=True, blank=True)
    default_color = ColorField(null=True, blank=True, help_text='Color for this location in calendar')


class BusinessHour(models.Model):
    class Meta:
        unique_together = (('work_location_object', 'day'),)

    DAY_CHOICES = [
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    ]

    work_location_object = models.ForeignKey(WorkLocation, on_delete=models.CASCADE, null=False, blank=False)
    day = models.IntegerField(choices=DAY_CHOICES, null=False, blank=False)
    start_at = models.TimeField(null=True, blank=True)
    finish_at = models.TimeField(null=True, blank=True)
    