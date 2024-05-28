from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Addresses)
admin.site.register(models.EmployeeTypes)
admin.site.register(models.EmployeeInformations)
admin.site.register(models.Images)
admin.site.register(models.Notes)
admin.site.register(models.ChangeLogs)
