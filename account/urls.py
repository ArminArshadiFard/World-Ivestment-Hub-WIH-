from django.urls import path, include
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path("login", login_view, name="login"),
    path("logout_view", logout_view, name="logout"),
    path("register", register, name="register"),
    path("email_validation", email_validation, name="email_validation"),
    path("profile", profile, name="profile"),
    path('change_password/', change_password, name="change_password"),

    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
