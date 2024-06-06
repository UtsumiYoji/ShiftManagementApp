from django.views import generic
from django.forms import modelformset_factory
from django.urls import reverse_lazy


from . import models, forms

# Create your views here.
class StoreCreateView(generic.CreateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Store'
        return context


class StoreListView(generic.ListView):
    model = models.Store
    template_name = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store List'
        return context
    

class StoreUpdateView(generic.UpdateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Store'
        return context
    

class StoreDeleteView(generic.DeleteView):
    model = models.Store
    template_name = ''
    success_url = reverse_lazy('')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Store'
        return context


