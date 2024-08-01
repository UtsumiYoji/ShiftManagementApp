from django.urls import path
from . import views

app_name = 'shift'

urlpatterns = [
    # path('', views.ListWorkLocationView.as_view(), name='work_location-list'),
    path('create/work_location', views.CreateWorkLocationView.as_view(), name='work_location-create'),
    path('create/shift', views.CreateShiftView.as_view(), name='shift-create'),
]