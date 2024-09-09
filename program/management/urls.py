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
    path('users/', views.ListUserView.as_view(), name='user_list'),
    path('users/<int:pk>', views.DetailUserView.as_view(), name='user_detail'),
    path('users/<int:pk>/employee_information', views.UpdateEmployeeInformationView.as_view(), name='employee_information'),
    path('users/<int:pk>/image', views.CreateImageView.as_view(), name='image'),
    path('users/<int:pk>/image/<int:image_id>/delete', views.DeleteImageView.as_view(), name='delete_image'),
    path('users/<int:pk>/note', views.CreateNoteView.as_view(), name='note'),
    path('users/<int:pk>/note/<int:note_id>/delete', views.DeleteNoteView.as_view(), name='delete_note'),
    path('users/<int:pk>/left', views.DateLeftView.as_view(), name='user_left'),
]