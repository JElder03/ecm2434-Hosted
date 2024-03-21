"""
Author: Jamie Elder
Defines how to render all pages starting with /recipes/
"""

from django.urls import path

from . import views

app_name = "recipes"
urlpatterns = [
    path("create", views.create_recipe, name="create_recipe"),
    path("<int:recipe_id>", views.view_recipe, name="view_recipe"),
    path("", views.view_all_recipes, name="view_all_recipes"),
]
