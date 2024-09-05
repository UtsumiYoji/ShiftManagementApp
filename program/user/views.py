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
    success_url = reverse_lazy('user:user')

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
    success_url = reverse_lazy('user:user')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView(views.PasswordChangeView):
    form_class = auth_forms.PasswordChangeForm
    success_url = reverse_lazy('user:user')
    template_name = 'user/password.html'


class DeleteUserView(generic.DeleteView):
    model = models.User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user:sign-up')

    def get_object(self, queryset=None):
        return self.request.user


class AddressView(CustomPermissionMixin, generic.UpdateView):
    model = models.Address
    form_class = forms.AddressForm
    template_name = 'user/address.html'
    success_url = reverse_lazy('user:address')

    def get_object(self, queryset=None):
        return getattr(self.request.user, 'address', None)

    def form_valid(self, form):
        form.instance.user_object = self.request.user
        return super().form_valid(form)
    

class BankInformationView(CustomPermissionMixin, generic.UpdateView):
    model = models.BankInformation
    form_class = forms.BankInformationForm
    template_name = 'user/bank_information.html'
    success_url = reverse_lazy('user:bank_information')

    def get_object(self, queryset=None):
        return getattr(self.request.user, 'bankinformation', None)
    
    def form_valid(self, form):
        form.instance.user_object = self.request.user
        return super().form_valid(form)
