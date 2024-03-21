"""
Author: Jamie Elder
"""

from django import forms
from datetime import datetime
from recipes.models import Recipe
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget
from django.utils import timezone


def not_in_past(date_time):
    """
    A custom requirement to check a if a date is in the past. Used to ensure cooking events are not
    created with dates in the past.

    # Parameters
    date_time (datetime): The datetime to be checked

    # Throws
    ValidationError: If date_time is in the past
    """
    if timezone.now() >= date_time:
        raise ValidationError("Your event date cannot be in the past")


class CreateMealEvent(forms.Form):
    """
    A form for creating a new meal event
    """

    # Get a list of all the recipe ids and titles 
    recipe_choices = []
    for recipe in Recipe.objects.all():
        recipe_choices.append((recipe.recipe_id, recipe.recipe_title))

    # Create meal event form fields
    recipe = forms.ChoiceField(choices=recipe_choices)
    date_time = forms.DateTimeField(
        validators=[not_in_past],
        # Use widget for calendar like selection of a date
        widget=forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
    )


class createGroupForm(forms.ModelForm):
    """
    Form fro creating a new group. Gets a name input.
    """
    class Meta:
        model = Group
        fields = ["name"]
