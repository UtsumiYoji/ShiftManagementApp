from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms
from user import models as user_models


class CheckAccessAuthorization(LoginRequiredMixin):
    redirect_to = reverse_lazy('management:top_page')
    restricted_page_url = '/management/'

    def dispatch(self, request, *args, **kwargs):
        # make sure user already logined or not
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # get current url and user
        user = self.request.user

        # if user is staff, it can access
        if user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # make sure user has authorization
        query = models.UserAccessAuthorization.objects.select_related(
            'restricted_page_object').filter(
                user_object=user, restricted_page_object__url__contains=self.restricted_page_url)
        if query:
            return super().dispatch(request, *args, **kwargs)

        # make sure user has employee information
        if not hasattr(user, 'employeeinformation'):
            return redirect(self.redirect_to)
        
        # make sure user has type
        if not user.employeeinformation.employee_type_object:
            return redirect(self.redirect_to)

        # make type of user has authorization
        type = self.request.user.employeeinformation.employee_type_object
        query = models.EmployeeTypeAccessAuthorization.objects.select_related(
            'restricted_page_object').filter(
                employee_type_object=type, restricted_page_object__url__contains=self.restricted_page_url)
        if query:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect(self.redirect_to)


class ManagementTopPageView(CheckAccessAuthorization, generic.TemplateView):
    template_name = 'management/top_page.html'
    restricted_page_url = reverse_lazy('common:top_page')


class CreateUserAccessAuthorizationView(CheckAccessAuthorization, generic.CreateView):
    model = models.UserAccessAuthorization
    form_class = forms.UserAccessAuthorizationsForm
    template_name = 'management/access_authorization/create.html'
    restricted_page_url = '/management/access_authorization/'
    success_url = reverse_lazy('management:user_access')


class CreateEmployeeTypeAccessAuthorizationView(CheckAccessAuthorization, generic.CreateView):
    model = models.EmployeeTypeAccessAuthorization
    form_class = forms.EmployeeTypeAccessAuthorizationsForm
    template_name = 'management/access_authorization/create.html'
    restricted_page_url = '/management/access_authorization/'
    success_url = reverse_lazy('management:employeetype_access')


class ListUserAccessAuthorizationsView(CheckAccessAuthorization, generic.ListView):
    model = models.UserAccessAuthorization
    template_name = 'management/access_authorization/list_user.html'
    restricted_page_url = '/management/access_authorization/'


class ListEmployeeTypeAccessAuthorizationView(CheckAccessAuthorization, generic.ListView):
    model = models.EmployeeTypeAccessAuthorization
    template_name = 'management/access_authorization/list_employee_type.html'
    restricted_page_url = '/management/access_authorization/'


class UpdateUserAccessAuthorizationView(CheckAccessAuthorization, generic.UpdateView):
    model = models.UserAccessAuthorization
    form_class = forms.UserAccessAuthorizationsForm
    template_name = 'management/access_authorization/create.html'
    restricted_page_url = '/management/access_authorization/'
    success_url = reverse_lazy('management:user_access')


class UpdateEmployeeTypeAccessAuthorizationView(CheckAccessAuthorization, generic.UpdateView):
    model = models.EmployeeTypeAccessAuthorization
    form_class = forms.EmployeeTypeAccessAuthorizationsForm
    template_name = 'management/access_authorization/create.html'
    restricted_page_url = '/management/access_authorization/'
    success_url = reverse_lazy('management:employeetype_access')


class DeleteUserAccessAuthorizationView(CheckAccessAuthorization, generic.DeleteView):
    model = models.UserAccessAuthorization
    template_name = 'management/access_authorization/delete.html'
    restricted_page_url = '/management/access_authorization/'
    success_url = reverse_lazy('management:user_access')


class DeleteEmployeeTypeAccessAuthorizationView(CheckAccessAuthorization, generic.DeleteView):
    model = models.EmployeeTypeAccessAuthorization
    template_name = 'management/access_authorization/delete.html'
    restricted_page_url = '/management/access_authorization/'
    success_url = reverse_lazy('management:employeetype_access')


class ListUserView(generic.ListView):
    model = user_models.User
    template_name = 'management/list_user.html'
