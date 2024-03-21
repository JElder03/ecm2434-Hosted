"""
Author: Jamie Elder

Define how all links starting with /accounts/ are handled
"""

from django.urls import path

from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('register/', views.register, name='register'),
    path("terms/", views.terms, name = 'terms'),
    path('login/', auth.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='users/logout.html', next_page=None), name='logout'),
    path('delete_account/', views.delete_user, name='delete_user'),
    path("password_reset/", auth.PasswordResetView.as_view(template_name='users/password_reset.html', email_template_name='users/password_reset_html_email.html'), name="password_reset"),
    path("password_reset_done/", auth.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>", auth.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password_reset_complete/", auth.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
]
