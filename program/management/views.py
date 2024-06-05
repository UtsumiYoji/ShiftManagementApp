from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms
from common.shortcuts import get_object_or_none, get_list_or_none
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


class ListUserView(CheckAccessAuthorization, generic.ListView):
    model = user_models.User
    restricted_page_url = '/management/user_information/'
    template_name = 'management/list.html'


class CreateUpdateEmployeeInformationView(CheckAccessAuthorization, generic.View):
    template_name = ''
    restricted_page_url = '/management/user_information/'
    success_url = reverse_lazy('management:top_page')

    def get(self, request, *args, **kwargs):
        objects = dict()

        # Get user information
        user = get_object_or_none(user_models.User, pk=kwargs['pk'])
        objects['user'] = user
        objects['address'] = get_object_or_none(user_models.Address, user_object=user)
        objects['bank'] = get_object_or_none(user_models.BankInformation, user_object=user)
        objects['images'] = get_list_or_none(user_models.Image, user_object=user)
        objects['notes'] = get_list_or_none(user_models.Note, user_object=user)

        # Make forms
        if hasattr(user, 'employeeinformation'):
            objects['employee_form'] = forms.EmployeeInformationForm(instance=user.employeeinformation)
        else: 
            objects['employee_form'] = forms.EmployeeInformationForm()

        return self.render_to_response(objects)

    def post(self, request, *args, **kwargs):
        objects = dict()

        # Get user information
        user = get_object_or_none(user_models.User, pk=kwargs['pk'])
        objects['user'] = user
        objects['address'] = get_object_or_none(user_models.Address, user_object=user)
        objects['bank'] = get_object_or_none(user_models.BankInformation, user_object=user)
        objects['images'] = get_list_or_none(user_models.Image, user_object=user)
        objects['notes'] = get_list_or_none(user_models.Note, user_object=user)

        # Make forms
        if hasattr(user, 'employeeinformation'):
            objects['employee_form'] = forms.EmployeeInformationForm(request.POST, instance=user.employeeinformation)
        else: 
            objects['employee_form'] = forms.EmployeeInformationForm(request.POST)

        if objects['employee_form'].is_valid():
            objects['employee_form'].instance.user_object = user
            objects['employee_form'].save()
            return redirect(self.success_url)

        return self.render_to_response(objects)

    def render_to_response(self, context):
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context))
    

class CreateImageView(CheckAccessAuthorization, generic.CreateView):
    model = user_models.Image
    form_class = forms.ImageForm
    template_name = ''
    restricted_page_url = '/management/user_information/'
    success_url = reverse_lazy('management:user_information')


class CreateNoteView(CheckAccessAuthorization, generic.CreateView):
    model = user_models.Note
    form_class = forms.NoteForm
    template_name = ''
    restricted_page_url = '/management/user_information/'
    success_url = reverse_lazy('management:user_information')
