from django.urls import path
from . import views

app_name = 'work_location'

urlpatterns = [
    path('', views.ListWorkLocationView.as_view(), name='list'),

    # User access authorization
    path('create/', views.CreateWorkLocationView.as_view(), name='create'),
    path('<int:pk>/', views.UpdateWorkLocationView.as_view(), name='update'),
]