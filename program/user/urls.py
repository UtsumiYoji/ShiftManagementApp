from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'user'
urlpatterns = [
    path('sign-up/', views.CreateUserView.as_view(), name='sign-up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', views.UpdateUserView.as_view(), name='user-update'),
    path('password/', views.PasswordChangeView.as_view(), name='password'),
    # path('delete/', views.DeleteUserView.as_view(), name='user-delete'),

    path('address/create/', views.CreateAddressView.as_view(), name='address-create'),
    path('address/', views.UpdateAddressView.as_view(), name='address-update'),

    path('bank_information/create/', views.CreateBankInformationView.as_view(), name='employee_information-create'),
    path('bank_information/', views.UpdateBankInformationView.as_view(), name='employee_information-update'),
]