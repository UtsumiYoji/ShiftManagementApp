from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import redirect
from common.shortcuts import get_object_or_none
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms
from user import models as user_models


# Base from
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


# top page
class ManagementTopPageView(CheckAccessAuthorization, generic.TemplateView):
    template_name = 'management/top_page.html'
    restricted_page_url = reverse_lazy('common:top_page')


# From here, form for manage access authorization
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


# From here, it is for user
class ListUserView(generic.ListView):
    model = user_models.User
    template_name = 'management/user/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        for object in queryset:
            object.information = 'Incomplete'
            if hasattr(object, 'bankinformation') and hasattr(object, 'employeeinformation'):
                object.information = 'Complete'
        
        return queryset
    

class DetailUserView(generic.DetailView):
    model = user_models.User
    template_name = "management/user/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank_information'] = get_object_or_none(user_models.BankInformation, user_object=self.object)
        context['employee_information'] = get_object_or_none(user_models.EmployeeInformation, user_object=self.object)
        context['address'] = get_object_or_none(user_models.Address, user_object=self.object)
        context['images'] = user_models.Image.objects.filter(user_object=self.object)
        context['notes'] = user_models.Note.objects.filter(user_object=self.object)

        return context
    

class UpdateEmployeeInformationView(generic.UpdateView):
    model = user_models.EmployeeInformation
    form_class = forms.EmployeeInformationForm
    template_name = 'management/user/employee_information.html'
    success_url = 'management:user_detail'

    def get_object(self, queryset=None):
        return get_object_or_none(
            user_models.EmployeeInformation,
            user_object=user_models.User.objects.get(pk=self.kwargs.get('pk'))
        )

    def form_valid(self, form):
        form.instance.user_object = user_models.User.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(self.success_url, kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['user'] = user_models.User.objects.get(pk=pk)
        return context


class CreateImageView(generic.CreateView):
    model = user_models.Image
    form_class = forms.ImageForm
    template_name = 'management/user/image.html'
    success_url = 'management:user_detail'

    def form_valid(self, form):
        form.instance.user_object = user_models.User.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(self.success_url, kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['user'] = user_models.User.objects.get(pk=pk)
        return context


class DeleteImageView(generic.DeleteView):
    model = user_models.Image
    success_url = 'management:user_detail'

    def get_success_url(self) -> str:
        return reverse(self.success_url, kwargs={'pk': self.kwargs.get('pk')})

    def get_object(self, queryset=None):
        return get_object_or_none(user_models.Image, pk=self.kwargs.get('image_id'))

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())


class CreateNoteView(generic.CreateView):
    model = user_models.Note
    form_class = forms.NoteForm
    template_name = 'management/user/note.html'
    success_url = 'management:user_detail'

    def form_valid(self, form):
        form.instance.user_object = user_models.User.objects.get(pk=self.kwargs.get('pk'))
        form.instance.editor_object = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(self.success_url, kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['user'] = user_models.User.objects.get(pk=pk)
        return context
    

class DeleteNoteView(generic.DeleteView):
    model = user_models.Note
    success_url = 'management:user_detail'

    def get_success_url(self) -> str:
        return reverse(self.success_url, kwargs={'pk': self.kwargs.get('pk')})

    def get_object(self, queryset=None):
        return get_object_or_none(user_models.Note, pk=self.kwargs.get('note_id'))

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())
    

class DateLeftView(generic.UpdateView):
    model = user_models.User
    form_class = forms.DateLeftForm
    success_url = 'management:user_detail'
    template_name = 'management/user/user_left.html'

    def get_success_url(self) -> str:
        return reverse(self.success_url, kwargs={'pk': self.kwargs.get('pk')})
    
    def get_object(self, queryset=None):
        return get_object_or_none(user_models.User, pk=self.kwargs.get('pk'))