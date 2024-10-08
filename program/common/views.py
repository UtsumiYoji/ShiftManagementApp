from datetime import datetime
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from management import models as management_models
from shift import models as shift_models

# Create your views here.
# Base from
class CheckAccessAuthorization(LoginRequiredMixin):
    redirect_to = reverse_lazy('common:top_page')
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
        query = management_models.UserAccessAuthorization.objects.select_related(
            'restricted_page_object').filter(
                user_object=user, restricted_page_object__url__contains=self.restricted_page_url)
        if query:
            return super().dispatch(request, *args, **kwargs)

        # make sure user has employee information
        if not hasattr(user, 'employeeinformation'):
            return redirect(f'{self.redirect_to}?access=denied')
        
        # make sure user has type
        if not user.employeeinformation.employee_type_object:
            return redirect(f'{self.redirect_to}?access=denied')

        # make type of user has authorization
        type = self.request.user.employeeinformation.employee_type_object
        query = management_models.EmployeeTypeAccessAuthorization.objects.select_related(
            'restricted_page_object').filter(
                employee_type_object=type, restricted_page_object__url__contains=self.restricted_page_url)
        if query:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect(f'{self.redirect_to}?access=denied')


class TopPageView(generic.ListView):
    model = shift_models.UserShift
    template_name = 'common/top_page.html'

    def get_queryset(self):
        
        queryset = shift_models.UserShift.objects.filter(
            user_object_id=self.request.user.id,
            start_at__gte=datetime.today()
        ).order_by('start_at')[:7]

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context