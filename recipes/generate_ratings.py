"""
Author: Jamie Elder
Program for populating ingredients database. Run once manually on database initialisation.
"""
from recipes.models import IngredientRating

ratings = (
    ('Beef', 365),
    ('Fish', 301, 'fish'),
    ('Prawns', 227, 'crustaceans'),
    ('Cheese', 98, 'milk'),
    ('Lamb', 97),
    ('Pork', 76, 'pork'),
    ('Chicken', 49),
    ('Rice', 35),
    ('Egg', 22, 'egg'),
    ('Nuts', 19, 'nuts'),
    ('Milk', 11, 'milk'),
    ('Peas', 8),
    ('Tomatoes', 8),
    ('Flour', 7, 'gluten'),
    ('Banana', 3),
    ('Citrus', 2),
    ('Apple', 1)
               )

for rating in ratings:
    i = IngredientRating(ingredient = rating[0], rating = rating[1])
    i.save()