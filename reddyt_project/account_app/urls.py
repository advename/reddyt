from django.urls import path
from . import views

app_name = 'account_app'

urlpatterns = [
    path('', views.login, name="login"),
    path('user/', views.user, name="user"),
    path('sign-up/', views.sign_up, name="sign_up"),
    path('update-password/', views.update_password, name="update_password"),
    path('logout/', views.logout, name="logout"),
    path('delete/', views.delete, name="delete"),
    path('request-reset-token/', views.request_reset_token,
         name="request_reset_token"),
    path('reset-password/', views.reset_password,
         name="reset_password"),
]
