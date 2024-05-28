from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Stores)
admin.site.register(models.BusinessHours)
admin.site.register(models.ChangeLog)
admin.site.register(models.Employees)
admin.site.register(models.ShiftManagers)