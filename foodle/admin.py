"""
Author: Jamie Elder
"""
from django.contrib import admin

from recipes.models import Recipe, IngredientRating
from .models import MealEvent
from users.models import UserProfile

# Allow game masters access to chosen databases
admin.site.register(IngredientRating)
admin.site.register(Recipe)
admin.site.register(UserProfile)
admin.site.register(MealEvent)