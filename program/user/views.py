from django.contrib.auth import views, login
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import mixins
from django.urls import reverse_lazy
from django.views import generic

from . import models, forms
from common.views import CustomPermissionMixin

# Create your views here.
class CreateUserView(generic.CreateView):
    model = models.User
    form_class = forms.UserCreationForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user-update')

    def form_valid(self, form):
        ret = super().form_valid(form)
        login(self.request, self.object)
        return ret


class LoginView(views.LoginView):
    template_name = 'user/login.html'
    form_class = auth_forms.AuthenticationForm


class UpdateUserView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.User
    form_class = forms.UserChangeForm
    template_name = 'user/update.html'
    success_url = reverse_lazy('user:user-update')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView(views.PasswordChangeView):
    form_class = auth_forms.PasswordChangeForm
    success_url = reverse_lazy('user:user-update')
    template_name = 'user/password.html'


class DeleteUserView(generic.DeleteView):
    model = models.User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user:sign-up')

    def get_object(self, queryset=None):
        return self.request.user
    

class CreateAddressView(CustomPermissionMixin, generic.CreateView):
    model = models.Addresses
    form_class = forms.AddressForm
    template_name = 'user/address.html'
    field_not_required = 'addresses'
    success_url = reverse_lazy('user:address-update')
    redirect_to = reverse_lazy('user:address-update')

    # add user_object to instance before saving
    def form_valid(self, form):
        form.instance.user_object = self.request.user
        return super().form_valid(form)
    

class UpdateAddressView(CustomPermissionMixin, generic.UpdateView):
    model = models.Addresses
    form_class = forms.AddressForm
    template_name = 'user/address.html'
    field_required = 'addresses'
    redirect_to = reverse_lazy('user:address-create')
    success_url = reverse_lazy('user:address-update')

    def get_object(self, queryset=None):
        return self.request.user.addresses
    

class CreateEmployeeInformationView(CustomPermissionMixin, generic.CreateView):
    model = models.EmployeeInformations
    form_class = forms.EmployeeInformationForm
    template_name = 'user/employee_information.html'
    field_not_required = 'employeeinformations'
    success_url = reverse_lazy('user:employee_information-update')
    redirect_to = reverse_lazy('user:employee_information-update')

    # add user_object to instance before saving
    def form_valid(self, form):
        form.instance.user_object = self.request.user
        return super().form_valid(form)
    

class UpdateEmployeeInformationView(CustomPermissionMixin, generic.UpdateView):
    model = models.EmployeeInformations
    form_class = forms.EmployeeInformationForm
    template_name = 'user/employee_information.html'
    field_required = 'employeeinformations'
    redirect_to = reverse_lazy('user:employee_information-create')
    success_url = reverse_lazy('user:employee_information-update')

    def get_object(self, queryset=None):
        return self.request.user.employeeinformations

