from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Address)
admin.site.register(models.BankInformation)
admin.site.register(models.EmployeeType)
admin.site.register(models.EmployeeInformation)
admin.site.register(models.Image)
admin.site.register(models.Note)
admin.site.register(models.Log)
