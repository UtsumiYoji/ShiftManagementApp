from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.ManagementTopPageView.as_view(), name='top_page'),

    path('user_access/create/', views.CreateUserAccessAuthorizationView.as_view(), name='user_access-create'),
    path('user_access/', views.ListUserAccessAuthorizationsView.as_view(), name='user_access'),

    path('employeetype_access/create/', views.CreateEmployeeTypeAccessAuthorizationView.as_view(), name='employeetype_access-create'),
    path('employeetype_access/', views.ListEmployeeTypeAccessAuthorizationView.as_view(), name='employeetype_access'),
]