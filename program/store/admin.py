from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Store)
admin.site.register(models.BusinessHour)
admin.site.register(models.Employee)
admin.site.register(models.Manager)
