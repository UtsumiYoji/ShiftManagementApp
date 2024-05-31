from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
# this class is for taking over by others
class CustomPermissionMixin(LoginRequiredMixin):
    field_required = None
    field_not_required = None
    redirect_to = reverse_lazy('user:login')

    def dispatch(self, request, *args, **kwargs):
        # make sure user already logined or not
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # make sure user has data of specific field
        if self.field_required:
            if not self.has_field(self.field_required):
                return redirect(self.redirect_to)
    
        # make sure user has data of specific field
        if self.field_not_required:
            if self.has_field(self.field_not_required):
                return redirect(self.redirect_to)

        return super().dispatch(request, *args, **kwargs)

    def has_field(self, field_name):
        return hasattr(self.request.user, field_name)
    

class TopPageView(generic.TemplateView):
    template_name = 'common/top_page.html'