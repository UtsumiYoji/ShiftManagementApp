from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.ListStoreView.as_view(), name='store-list'),

    # User access authorization
    path('store/create/', views.CreateStoreView.as_view(), name='store-create'),
    path('store/<int:pk>', views.UpdateStoreView.as_view(), name='store-update'),
    path('store/<int:pk>/businesshour', views.BusinnessHourView.as_view(), name='store_businesshour'),
    path('store/<int:pk>/delete', views.DeleteStoreView.as_view(), name='store-delete'),

]