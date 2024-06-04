from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.ManagementTopPageView.as_view(), name='top_page'),

    # User access authorization
    path('access_authorization/user/create/', views.CreateUserAccessAuthorizationView.as_view(), name='user_access-create'),
    path('access_authorization/user/', views.ListUserAccessAuthorizationsView.as_view(), name='user_access'),
    path('access_authorization/user/<int:pk>', views.UpdateUserAccessAuthorizationView.as_view(), name='user_access-update'),
    path('access_authorization/user/<int:pk>/delete', views.DeleteUserAccessAuthorizationView.as_view(), name='user_access-delete'),

    path('access_authorization/employeetype/create/', views.CreateEmployeeTypeAccessAuthorizationView.as_view(), name='employeetype_access-create'),
    path('access_authorization/employeetype/', views.ListEmployeeTypeAccessAuthorizationView.as_view(), name='employeetype_access'),
    path('access_authorization/employeetype/<int:pk>', views.UpdateEmployeeTypeAccessAuthorizationView.as_view(), name='employeetype_access-update'),
    path('access_authorization/employeetype/<int:pk>/delete', views.DeleteEmployeeTypeAccessAuthorizationView.as_view(), name='employeetype_access-delete'),

    # User information
    path('user_information/<int:pk>', views.CreateUpdateEmployeeInformationView.as_view(), name='user_information'),
]