from django.contrib.auth.views import (
    PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView, PasswordChangeView,
    PasswordChangeDoneView)
from django.urls import path, reverse_lazy
from . import views

app_name = "users"

urlpatterns = [
    path("signin/", views.UserLoginView.as_view(), name="login"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("signup/", views.UserRegistrationView.as_view(), name="signup"),
    path("<str:username>/update/", views.profile_update, name="edit"),
    path("logout/", views.user_logout, name="logout"),

    # Reset password
    path("password-reset/", PasswordResetView.as_view(
        template_name="password_reset_form.html",
        email_template_name="password_reset_email.html",
        success_url=reverse_lazy("users:password_reset_done")), name="password_reset"),
    path("password-reset/done/", PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"
    ), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html",
        success_url=reverse_lazy("users:password_reset_complete")), name="password_reset_confirm"),
    path("password-reset/complete/", PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"
    ), name="password_reset_complete"),

    # Email verification
    path('send-confirmation-email/', views.send_confirmation_email, name='send_confirmation_email'),
    path('confirm-email/<str:token>/', views.confirm_email, name='confirm_email'),

    # Password change
    path('password/', PasswordChangeView.as_view(
        template_name="password_change_form.html",
        success_url=reverse_lazy("users:password_reset_done")
    ), name='password_change'),
    path('password/done/', PasswordChangeDoneView.as_view(
        template_name="password_change_done.html"
    ), name='password_change_done')
]
