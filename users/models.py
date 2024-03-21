"""
Author: Jamie Elder
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime 
from foodle.models import MealEvent

class UserProfile(models.Model):
    """
    Define the database design of the user profile. User profiles extend the built in users
    to include other information, such as foodle score.
    """
    user = models.OneToOneField(User, on_delete = models.CASCADE)  
    foodle_score = models.IntegerField(default=0)

    def get_env_score(self):
        """
        Calculate the environmental score by summing the scores of every meal event of a user's group.
        """
        score = 0
        if (self.user.groups.count() == 0 ):
            return 0
        else:
            for event in MealEvent.objects.filter(group = self.user.groups.first()):
                score += event.score
        return score
    
    env_score = property(get_env_score) # make this a calculated attribute, re-calculated whenever read

    def __str__(self):  
          return "%s's profile: Score %d" % (self.user, self.foodle_score)

def create_user_profile(sender, instance, created, **kwargs):  
    """
    Creates a corresponding user profile for every base user created
    """
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)