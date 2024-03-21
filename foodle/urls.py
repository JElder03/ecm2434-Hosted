"""
Author: Jamie Elder

Define how all links starting with /foodle/ are handled
"""

from django.urls import path

from . import views

app_name = "foodle"
urlpatterns = [
    path("welcome/", views.welcome, name="welcome"),
    path("home/", views.home, name="home"),
    path("play/", views.play, name="play"),
    path("group-cooks/", views.events, name="events"),
    path("group-cooks/create", views.create_event, name="create_event"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("createGroup", views.createGroup, name="createGroup"),
    path("generateQrCode", views.generateQrCode, name="generateQrCode"),
    path("no_group/", views.no_group, name="no_group"),
]
