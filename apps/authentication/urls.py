from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    TokenObtainPairView, RegisterAccountView, VerifyAccountView, UpdatePasswordView, RequestPasswordRestoreView,
    PasswordRestoreView, VerifyRequestPasswordRestoreView
)

urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterAccountView.as_view()),
    path("register/verify", VerifyAccountView.as_view()),
    path("change_password/", UpdatePasswordView.as_view()),
    path("password_restore/request/", RequestPasswordRestoreView.as_view()),
    path("password_restore/verify/", VerifyRequestPasswordRestoreView.as_view()),
    path("password_restore/", PasswordRestoreView.as_view()),
]
