import json
from datetime import datetime

from django.views import generic
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.forms import formset_factory

from . import models, forms
from user import models as user_models

class TopPageView(generic.TemplateView):
    template_name = 'common/top_page.html'


class CreateView(generic.edit.BaseFormView, generic.TemplateView):
    template_name = 'shift/create.html'
    success_url = reverse_lazy('shift:top_page')

    def get_context_data(self, **kwargs):
        result = kwargs
        result['users'] = list(user_models.User.objects.filter(
            date_left=None
        ).values('id', 'first_name'))
        result['work_locations'] = models.WorkLocation.objects.filter(
            disabled=False
        )
        
        return result

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST['data'])
        
        user_shift_data = {
            'form-TOTAL_FORMS': len(data),
            'form-INITIAL_FORMS': 0,
        }
        break_time_data = {
            'form-INITIAL_FORMS': 0,
        }

        for i, d in enumerate(data):
            user_object = user_models.User.objects.get(id=d['user_id'])
            if d['work_location_id'] == '0':
                work_location_object = None
            else:
                work_location_object = models.WorkLocation.objects.get(id=d['work_location_id'])
            
            user_shift_data['form-'+str(i)+'-user_object'] = user_object
            user_shift_data['form-'+str(i)+'-work_location_object'] = work_location_object
            user_shift_data['form-'+str(i)+'-start_at'] = datetime.strptime(d['start_at'], '%Y-%m-%d %H:%M')
            user_shift_data['form-'+str(i)+'-finish_at'] = datetime.strptime(d['finish_at'], '%Y-%m-%d %H:%M')

            for b in d['break_time']:
                break_time_data['form-'+str(len(break_time_data)-1)+'-start_at'] = datetime.strptime(b, '%Y-%m-%d %H:%M')

        user_shift_formset = formset_factory(
            form=forms.UserShiftForm,
            max_num=len(user_shift_data)
        )(user_shift_data)

        break_time_data['form-TOTAL_FORMS'] = len(break_time_data) - 1
        break_time_formset = formset_factory(
            form=forms.BreakTimeForm,
            max_num=len(break_time_data)
        )(break_time_data)

        if user_shift_formset.is_valid() and break_time_formset.is_valid():
            # Save user_shift_formset
            user_shift_objects = [form.save() for form in user_shift_formset]

            break_form_index = 0
            for i, break_count in enumerate([len(d['break_time']) for d in data]):
                user_shift_object = user_shift_objects[i]
                for _ in range(break_count):
                    break_time_formset.forms[break_form_index].instance.user_shift_object = user_shift_object
                    break_form_index += 1
                    
            [form.save() for form in break_time_formset]

            return JsonResponse({'url': self.success_url})
        else:
            return JsonResponse({'status': 'error'})