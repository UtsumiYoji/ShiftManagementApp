from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'user'
urlpatterns = [
    path('sign-up/', views.CreateUserView.as_view(), name='sign-up'),
    path('login/', views.LoginView.as_view(), name='log-in'),
    path('logout/', LogoutView.as_view(), name='log-out'),

    path('', views.UpdateUserView.as_view(), name='user'),
    path('password/', views.PasswordChangeView.as_view(), name='password'),
    # path('delete/', views.DeleteUserView.as_view(), name='user-delete'),

    path('address/', views.AddressView.as_view(), name='address'),

    path('bank_information/', views.BankInformationView.as_view(), name='bank_information'),
]