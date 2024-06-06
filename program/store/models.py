from django.db import models
from user.models import User


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    place_name = models.CharField(max_length=255, blank=True, null=True, help_text='If your store is inside of mall or something')
    address1 = models.CharField('adress1', help_text='Street name', max_length=255, null=True, blank=True)
    address2 = models.CharField('adress2', help_text='(Optional) building name', max_length=255, null=True, blank=True)
    city = models.CharField('city', help_text='or Town', max_length=255, null=True, blank=True)
    postal_code = models.CharField('postal code', max_length=255, null=True, blank=True)
    province = models.CharField('province', max_length=255, null=True, blank=True)


class BusinessHour(models.Model):
    class Meta:
        unique_together = (('store_object', 'day'),)

    DAY_CHOICES = [
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    ]

    store_object = models.ForeignKey(Store, on_delete=models.CASCADE, null=False, blank=False)
    day = models.IntegerField(choices=DAY_CHOICES, null=False, blank=False)
    start_at = models.TimeField(null=True, blank=True)
    finish_at = models.TimeField(null=True, blank=True)


class Employee(models.Model):
    class Meta:
        unique_together = (('store_object', 'user_object'),)

    store_object = models.ForeignKey(Store, on_delete=models.CASCADE, null=False, blank=False)
    user_object = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)


class Manager(models.Model):
    class Meta:
        unique_together = (('store_object', 'user_object'),)
    
    store_object = models.ForeignKey(Store, on_delete=models.CASCADE, null=False, blank=False)
    user_object = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    