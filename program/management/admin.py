from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.RestrictedPage)
admin.site.register(models.UserAccessAuthorization)
admin.site.register(models.EmployeeTypeAccessAuthorization)