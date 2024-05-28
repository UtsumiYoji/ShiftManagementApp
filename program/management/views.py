from django.views import generic

from . import models
from user import models as user_models
from common.views import CustomPermissionMixin


class UserAccessAuthorizationsCreate(generic.CreateView):
    pass


class EmployeeTypeAccessAuthorizationsForm(generic.CreateView):
    pass


class AccessAuthorizationList(generic.ListView):
    pass


# Create your views here.
class UserList(generic.ListView):
    pass