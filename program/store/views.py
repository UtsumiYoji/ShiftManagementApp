from django.db.models.query import QuerySet
from django.views import generic
from django.urls import reverse_lazy
from extra_views import ModelFormSetView

from . import models, forms

# Create your views here.
class CreateStoreView(generic.CreateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Store'
        return context


class ListStoreView(generic.ListView):
    model = models.Store
    template_name = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store List'
        return context
    

class UpdateStoreView(generic.UpdateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Store'
        return context
    

class DeleteStoreView(generic.DeleteView):
    model = models.Store
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Store'
        return context


class CreateBusinnessHourView(ModelFormSetView):
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

    def formset_valid(self, formset):
        store_object = models.Store.objects.get(pk=self.kwargs['pk'])
        for form in formset:
            form.instance.store_object = store_object
        return super().formset_valid(formset)


class UpdateBusinessHourView(ModelFormSetView):
    model = models.BusinessHour
    form_class = forms.BusinessHourForm
    queryset = models.BusinessHour.objects.none()
    template_name = ''
    success_url = reverse_lazy('')

    def get_queryset(self) -> QuerySet[models.BusinessHour]:
        return models.BusinessHour.objects.filter(store_object=self.kwargs['pk'])