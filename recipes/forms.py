"""
Author: Jamie Elder
"""

from django import forms
from .fields import CommaSeparatedStrings


class RecipeForm(forms.Form):
    """
    Defines information to be collected from  a user when creating a recipe. User, allergens,
    and sulphate score are calculated in backend.
    """

    recipe_title = forms.CharField(max_length=200)
    ingredients = CommaSeparatedStrings(widget=forms.HiddenInput())
    quantities = CommaSeparatedStrings(widget=forms.HiddenInput())
    preparation = forms.CharField()
    prep_time = forms.IntegerField(min_value=0, label="Prep Time (hrs)")
    serves_num = forms.IntegerField(min_value=0, label="Serves")
