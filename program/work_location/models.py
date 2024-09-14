from django.db import models
from colorfield.fields import ColorField


# Create your models here.
class WorkLocation(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    color = models.CharField(max_length=7, null=False, blank=False, help_text='Color for this location in calendar')
    place_name = models.CharField(max_length=255, blank=True, null=True, help_text='If your store is inside of mall or something')
    address1 = models.CharField(help_text='Street name', max_length=255, null=True, blank=True)
    address2 = models.CharField(help_text='(Optional) building name', max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    disabled = models.BooleanField(default=False, null=False, blank=False)
    made_on = models.DateField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.name

    