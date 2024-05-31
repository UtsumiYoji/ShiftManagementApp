from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms
from user import models as user_models


class CheckAccessAuthorization(LoginRequiredMixin):
    field_required = None
    field_not_required = None
    redirect_to = reverse_lazy('management:top_page')
    restricted_page_url = None

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


class ManagementTopPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'management/top_page.html'

    def dispatch(self, request, *args, **kwargs):
        # make sure user already logined or not
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # get user
        user = self.request.user

        # if user is staff, it can access
        if user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # make sure user has authorization
        query = models.UserAccessAuthorization.objects.select_related(
            'restricted_page_object').filter(
                user_object=user, restricted_page_object__url__contains='/management/')
        if query:
            return super().dispatch(request, *args, **kwargs)

        # make sure user has employee information
        if not hasattr(user, 'employeeinformation'):
            return redirect(reverse_lazy('common:top_page'))
        
        # make sure user has type
        if not user.employeeinformation.employee_type_object:
            return redirect(reverse_lazy('common:top_page'))

        # make type of user has authorization
        type = self.request.user.employeeinformation.employee_type_object
        query = models.EmployeeTypeAccessAuthorization.objects.select_related(
            'restricted_page_object').filter(
                user_object=user, restricted_page_object__url__contains='/management/')
        if query:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect(reverse_lazy('common:top_page'))


class CreateUserAccessAuthorizationView(CheckAccessAuthorization, generic.CreateView):
    model = models.UserAccessAuthorization
    form_class = forms.UserAccessAuthorizationsForm
    template_name = 'management/create_access_authorization.html'
    restricted_page_url = '/management/access_authorization/'
    success_url = reverse_lazy('management:user_access')


class CreateEmployeeTypeAccessAuthorizationView(CheckAccessAuthorization, generic.CreateView):
    model = models.EmployeeTypeAccessAuthorization
    form_class = forms.EmployeeTypeAccessAuthorizationsForm
    template_name = 'management/create_access_authorization.html'
    restricted_page_url = '/management/access_authorization/'
    success_url = reverse_lazy('management:employeetype_access')


class ListUserAccessAuthorizationsView(generic.ListView):
    model = models.UserAccessAuthorization
    template_name = 'management/user_access_authorization.html'


class ListEmployeeTypeAccessAuthorizationView(generic.ListView):
    model = models.EmployeeTypeAccessAuthorization
    template_name = 'management/employee_type_access_authorization.html'


class UpdateUserAccessAuthorizationView(CheckAccessAuthorization, generic.DeleteView):
    model = models.UserAccessAuthorization
    template_name = 'management/create_access_authorization.html'
    success_url = reverse_lazy('management:user_access')


class UpdateEmployeeTypeAccessAuthorizationView(CheckAccessAuthorization, generic.DeleteView):
    model = models.EmployeeTypeAccessAuthorization
    template_name = 'management/create_access_authorization.html'
    success_url = reverse_lazy('management:employeetype_access')


class DeleteUserAccessAuthorizationView(CheckAccessAuthorization, generic.DeleteView):
    model = models.UserAccessAuthorization
    template_name = 'management/create_access_authorization.html'
    success_url = reverse_lazy('management:user_access')


class DeleteEmployeeTypeAccessAuthorizationView(CheckAccessAuthorization, generic.DeleteView):
    model = models.EmployeeTypeAccessAuthorization
    template_name = 'management/create_access_authorization.html'
    success_url = reverse_lazy('management:employeetype_access')


class ListEmployeeInformationView(generic.ListView):
    model = user_models.EmployeeInformation
    template_name = 'management/employee_type_access_authorization.html'
