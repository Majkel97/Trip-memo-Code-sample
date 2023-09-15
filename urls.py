"""
This module contains a list of URL patterns for the Django application.

URL patterns are used to map URLs to views in the Django application. The patterns in this module are defined using regular expressions and include the URL path and the view function that should handle the request.

Functions:
* url: A function that defines a URL pattern.
* path: A function that defines a URL pattern using a path-like syntax.
* include: A function that includes the URL patterns from another module.

To define a URL pattern, use the url or path function to specify the URL path and the view function that should handle the request. The URL path can include named groups, which can be passed as arguments to the view function.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
    path(
        "signup/",
        views.signup,
        name="signup",
    ),
    path(
        "signin/",
        views.signin,
        name="signin",
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),
    path(
        "activate-user/<uidb64>/<token>",
        views.activate_user,
        name="activate",
    ),
    path(
        "delete_user_account",
        views.delete_user_account,
        name="delete_user_account",
    ),
    path(
        "change_password",
        views.change_password,
        name="change_password",
    ),
    path(
        "edit_user_data",
        views.edit_user_data,
        name="edit_user_data",
    ),
    path(
        "edit_user_additional_data",
        views.edit_user_additional_data,
        name="edit_user_additional_data",
    ),
    path(
        "password_reset_form/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="mails/password_reset_email.html",
        ),
        name="password_reset_form",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path(
        "resend_activation_link",
        views.resend_activation_link,
        name="resend_activation_link",
    ),
]
