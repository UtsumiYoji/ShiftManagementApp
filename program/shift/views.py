from django.views.generic import edit
from django.urls import reverse_lazy
from django.forms import modelformset_factory

from . import models, forms


class CreateWorkLocationView(edit.BaseFormView):
    template_name = 'shift/create_work_location.html'
    success_url = reverse_lazy('')

    def make_formset(self, model, form, request_post_data=None):
        if request_post_data is None:
            result = modelformset_factory(
                model=model,
                form=form,
                extra=1,
                max_num=2,
            )
        else:
            result = modelformset_factory(
                model=model,
                form=form,
                max_num=(request_post_data) # need to be updated
            )(
                request_post_data
                )

        return result

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['title'] = 'Create Work Location'
        result['work_places'] = models.WorkLocation.objects.all()

        if 'formset' not in kwargs:
            kwargs['formset'] = self.make_formset(
                models.WorkLocation, forms.WorkLocationForm)
        
        return result

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        formset = self.make_formset(
            models.WorkLocation, forms.WorkLocationForm, request.POST)

        if formset.is_valid():
            formset.save()
            return self.form_valid(formset)
        else:
            return self.render_to_response(
                self.get_context_data(formset=formset))


class CreateShiftView(edit.BaseFormView):
    template_name = 'shift/create_shift.html'
    success_url = reverse_lazy('')

    def make_formset(self, model, form, request_post_data=None):
        if request_post_data is None:
            result = modelformset_factory(
                model=model,
                form=form,
                extra=1,
                max_num=2,
            )
        else:
            result = modelformset_factory(
                model=model,
                form=form,
                max_num=(request_post_data) # need to be updated
            )(
                request_post_data
                )

        return result

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['title'] = 'Create shift'

        if 'user_shift_formset' not in kwargs:
            kwargs['user_shift_formset'] = self.make_formset(
                models.UserShift, forms.UserShiftForm)
            
        if 'break_time_form' not in kwargs:
            kwargs['break_time_form'] = self.make_formset(
                models.BreakTime, forms.BreakTimeForm)
        
        return result

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        user_shift_formset = self.make_formset(
            models.UserShift, forms.UserShiftForm, request.POST)
        
        break_time_formset = self.make_formset(
            models.BreakTime, forms.BreakTimeForm, request.POST)

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
