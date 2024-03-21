"""
Author: Jamie Elder
"""

from django.db import models
from django.contrib.auth.models import User 

class IngredientRating(models.Model):
    """
    Define the database structure for the database of ingredients database
    """
    ingredient_id = models.AutoField(primary_key=True)
    ingredient = models.CharField(max_length=255, unique=True)
    rating = models.IntegerField()
    allergen = models.CharField(max_length=20, null=True, default = None, blank=True)

class Recipe(models.Model):
    """
    Define the database structure for the database of recipes database
    """
    recipe_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    recipe_title = models.CharField(max_length=200)
    recipe_ingredients = models.TextField()
    preparation = models.TextField()
    prep_time = models.PositiveIntegerField(default=0)
    serves_num = models.PositiveIntegerField(default=1)
    sulphates_per_portion = models.PositiveIntegerField(default=0)
    allergens = models.CharField(max_length=50, null=True, default = None, blank=True)
    
    def __str__(self):
        return self.recipe_title