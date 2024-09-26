from django.urls import path
from . import views

app_name = 'shift'

urlpatterns = [
    path('', views.TopPageView.as_view(), name='top_page'),
    path('create', views.CreateView.as_view(), name='create'),
]