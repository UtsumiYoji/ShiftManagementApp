from django.views import generic
from django.urls import reverse_lazy
from django.forms import modelformset_factory

from . import models, forms


# Create your views here.
class CreateWorkLocationView(generic.CreateView):
    model = models.WorkLocation
    form_class = forms.WorkLocationForm
    template_name = 'work_location/create.html'
    success_url = reverse_lazy('')
    
    def make_formset(self, request_post_data=None):
        if request_post_data is None:
            result = modelformset_factory(
                model=models.BusinessHour,
                form=forms.BusinessHourForm,
                extra=7,
                max_num=7,
            )(
                initial=[
                {'day': 0}, {'day': 1}, {'day': 2}, {'day': 3},
                {'day': 4}, {'day': 5}, {'day': 6}, 
                ]
            )
        else:
            result = modelformset_factory(
                model=models.BusinessHour,
                form=forms.BusinessHourForm,
                extra=7,
                max_num=7
            )(
                request_post_data
                )

        return result

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['title'] = 'Create work location'

        if 'formset' not in kwargs:
            result['formset'] = self.make_formset()

        return result

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.make_formset(request.POST)

        if (form.is_valid() and formset.is_valid()):
            work_location = form.save()
            for form in formset:
                form.instance.work_location_object = work_location
            formset.save()

            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset))


class ListWorkLocationView(generic.ListView):
    model = models.WorkLocation
    template_name = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Work location List'
        return context


class UpdateWorkLocationView(generic.UpdateView):
    model = models.WorkLocation
    form_class = forms.WorkLocationForm
    template_name = ''
    success_url = reverse_lazy('')

    def make_formset(self, request_post_data=None):
        if request_post_data is None:
            result = modelformset_factory(
                model=models.BusinessHour,
                form=forms.BusinessHourForm,
                max_num=7,
            )(
                queryset=models.BusinessHour.objects.filter(
                    work_location_object=self.object)
            )
        else:
            result = modelformset_factory(
                model=models.BusinessHour,
                form=forms.BusinessHourForm,
                max_num=7
            )(
                request_post_data
                )

        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update work location'

        if 'formset' not in kwargs:
            kwargs['formset'] = self.make_formset()

        return context

    def post(self, request, *args: str, **kwargs):
        form = self.get_form()
        formset = self.make_formset(request.POST)

        if (form.is_valid() and formset.is_valid()):
            work_location = form.save()
            for form in formset:
                form.instance.work_location_object = work_location
            formset.save()

            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset))
    

class DeleteWorkLocationView(generic.DeleteView):
    model = models.WorkLocation
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete work location'
        return context
