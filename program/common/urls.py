from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('', views.TopPageView.as_view(), name='top_page'),
]