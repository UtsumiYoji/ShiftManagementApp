from django.urls import path
from . import views

app_name = 'shift'

urlpatterns = [
    path('', views.PrivateListView.as_view(), name='private_list'),
    path('create', views.CreateView.as_view(), name='create'),
]