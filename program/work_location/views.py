from django.views import generic
from django.urls import reverse_lazy
from django_filters import FilterSet, filters

from . import models, forms


# Create your views here.
class CreateWorkLocationView(generic.CreateView):
    model = models.WorkLocation
    form_class = forms.WorkLocationForm
    template_name = 'work_location/create.html'
    success_url = reverse_lazy('work_location:list')


class WorkLocationFilter(FilterSet):
    disabled = filters.BooleanFilter(method='filter_disabled')

    def filter_disabled(self, queryset, name, value):
        return queryset.filter(disabled=value)
    
    class Meta:
        model = models.WorkLocation
        fields = ['disabled', ]


class ListWorkLocationView(generic.ListView):
    model = models.WorkLocation
    template_name = 'work_location/list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return WorkLocationFilter(self.request.GET, queryset).qs


class UpdateWorkLocationView(generic.UpdateView):
    model = models.WorkLocation
    form_class = forms.WorkLocationForm
    template_name = 'work_location/update.html'
    success_url = reverse_lazy('work_location:list')

