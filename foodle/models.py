"""
Author: Jamie Elder
"""

from django.db import models
from django.contrib.auth.models import User, Group
from recipes.models import Recipe  

class MealEvent(models.Model):
    """
    Define the database structure for the database of meal events
    """
    
    Meal_Event_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    score = models.PositiveBigIntegerField(default = 0)