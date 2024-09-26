from django.db import models

from user import models as user_models
from work_location.models import WorkLocation

class UserShift(models.Model):
    user_object = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=False, blank=False)
    work_location_object = models.ForeignKey(WorkLocation, on_delete=models.CASCADE, null=False, blank=False)
    start_at = models.DateTimeField(null=False, blank=False)
    finish_at = models.DateTimeField(null=False, blank=False)
    note = models.CharField(max_length=100, null=True, blank=True)

class BreakTime(models.Model):
    user_object = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=False, blank=False)
    start_at = models.DateTimeField(null=False, blank=False)
    finish_at = models.DateTimeField(null=False, blank=False)