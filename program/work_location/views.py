from django.views import generic
from django.urls import reverse_lazy
from extra_views import ModelFormSetView

from . import models, forms


# Create your views here.
class CreateWorkLocationView(generic.CreateView):
    model = models.WorkLocation
    form_class = forms.WorkLocationForm
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create work location'
        return context


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update work location'
        return context
    

class DeleteWorkLocationView(generic.DeleteView):
    model = models.WorkLocation
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete work location'
        return context


class BusinnessHourView(ModelFormSetView):
    model = models.BusinessHour
    form_class = forms.BusinessHourForm
    factory_kwargs = {'extra': 6, 'max_num': 7}
    initial = [
                {'day': 0}, {'day': 1}, {'day': 2}, {'day': 3},
                {'day': 4}, {'day': 5}, {'day': 6}, 
            ]
    queryset = models.BusinessHour.objects.none()
    template_name = ''
    success_url = reverse_lazy('')

    def get_queryset(self):
        querys = models.BusinessHour.objects.filter(work_location_object=self.kwargs['pk'])
        if querys.exists():
            self.queryset = querys.values()
            del self.initial
        
        return super().get_queryset()

    def formset_valid(self, formset):
        work_location_object = models.WorkLocation.objects.get(pk=self.kwargs['pk'])
        for form in formset:
            form.instance.work_location_object = work_location_object
        return super().formset_valid(formset)
