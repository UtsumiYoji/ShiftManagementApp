from django.urls import path
from . import views

app_name = 'work_location'

urlpatterns = [
    path('', views.ListWorkLocationView.as_view(), name='work_location-list'),

    # User access authorization
    path('create/', views.CreateWorkLocationView.as_view(), name='work_location-create'),
    path('<int:pk>', views.UpdateWorkLocationView.as_view(), name='work_location-update'),
    path('<int:pk>/businesshour', views.BusinnessHourView.as_view(), name='work_location_businesshour'),
    path('<int:pk>/delete', views.DeleteWorkLocationView.as_view(), name='work_location-delete'),

]