from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.ListWorkLocationView.as_view(), name='work_location-list'),

    # User access authorization
    path('work_location/create/', views.CreateWorkLocationView.as_view(), name='work_location-create'),
    path('work_location/<int:pk>', views.UpdateWorkLocationView.as_view(), name='work_location-update'),
    path('work_location/<int:pk>/businesshour', views.BusinnessHourView.as_view(), name='work_location_businesshour'),
    path('work_location/<int:pk>/delete', views.DeleteWorkLocationView.as_view(), name='work_location-delete'),

]