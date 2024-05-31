from django.db import models
from user import models as user_models


# Create your models here.
class RestrictedPage(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    url = models.CharField(max_length=255, null=False, blank=False)
    
    def __str__(self) -> str:
        return self.name + ' (' + self.url + ')'


class UserAccessAuthorization(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_object", "restricted_page_object"],
                name="user_object-restricted_page_object"
            )]

    user_object = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=False, blank=False)
    restricted_page_object = models.ForeignKey(RestrictedPage, on_delete=models.CASCADE, null=False, blank=False)


class EmployeeTypeAccessAuthorization(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee_type_object", "restricted_page_object"],
                name="employee_type_object-restricted_page_object"
            )]

    employee_type_object = models.ForeignKey(user_models.EmployeeType, on_delete=models.CASCADE, null=False, blank=False)
    restricted_page_object = models.ForeignKey(RestrictedPage, on_delete=models.CASCADE, null=False, blank=False)