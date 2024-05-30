from django.db import models
from user import models as user_models


# Create your models here.
class UserAccessAuthorization(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_object", "url"],
                name="user_object-url"
            )]

    user_object = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=False, blank=False)
    url = models.CharField(max_length=255, null=False, blank=False)


class EmployeeTypeAccessAuthorization(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee_type_object", "url"],
                name="employee_type_object-url"
            )]

    employee_type_object = models.ForeignKey(user_models.EmployeeType, on_delete=models.CASCADE, null=False, blank=False)
    url = models.CharField(max_length=255, null=False, blank=False)