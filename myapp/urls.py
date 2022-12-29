from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# app_name = 'api'

urlpatterns = [
    path('user/register/', views.RegisterView.as_view(), name="register"),
    path('user/login/', views.LoginAPIView.as_view(), name="login"),
    path('user/logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('user/del/', views.DeleteAccountAPIView.as_view(), name="del"),
    path('user/<username>/new-password/', views.ChangePassWdAPIView.as_view(), name="new_password"),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
