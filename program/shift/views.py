from django.views import generic
from django.urls import reverse_lazy
from django.forms import formset_factory

from . import models, forms
from user import models as user_models

class TopPageView(generic.TemplateView):
    template_name = 'common/top_page.html'


class CreateView(generic.edit.BaseFormView, generic.TemplateView):
    template_name = 'shift/create.html'
    success_url = reverse_lazy('')

    def make_formset(self, form, request_post_data=None):
        if request_post_data is None:
            result = formset_factory(
                form=form,
                extra=1,
                max_num=2,
            )
        else:
            result = formset_factory(
                form=form,
                extra=1,
                max_num=(request_post_data) # need to be updated
            )(
                request_post_data
                )

        return result

    def get_context_data(self, **kwargs):
        result = kwargs
        result['users'] = list(user_models.User.objects.filter(
            date_left=None
        ).values('id', 'first_name'))
        result['work_locations'] = models.WorkLocation.objects.filter(
            disabled=False
        )

        if 'user_shift_formset' not in kwargs:
            kwargs['user_shift_formset'] = self.make_formset(
                forms.UserShiftForm
                )
            
        if 'break_time_form' not in kwargs:
            kwargs['break_time_form'] = self.make_formset(
                forms.BreakTimeForm
                )
        
        return result

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        user_shift_formset = self.make_formset(
            forms.UserShiftForm, request.POST)
        
        break_time_formset = self.make_formset(
            forms.BreakTimeForm, request.POST)

        if (user_shift_formset.is_valid() and break_time_formset.is_valid()):
            user_shift_formset.save()
            break_time_formset.save()
            return self.form_valid(user_shift_formset)
        else:
            return self.render_to_response(
                self.get_context_data(
                    user_shift_formset=user_shift_formset, 
                    break_time_form=break_time_formset
                    ))
