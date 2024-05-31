from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.ManagementTopPageView.as_view(), name='top_page'),

    path('access_authorization/user/create/', views.CreateUserAccessAuthorizationView.as_view(), name='user_access-create'),
    path('access_authorization/user/', views.ListUserAccessAuthorizationsView.as_view(), name='user_access'),

    path('access_authorization/employeetype/create/', views.CreateEmployeeTypeAccessAuthorizationView.as_view(), name='employeetype_access-create'),
    path('access_authorization/employeetype/', views.ListEmployeeTypeAccessAuthorizationView.as_view(), name='employeetype_access'),
]