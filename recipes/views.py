"""
Author: Jamie Elder, Victor Smith
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Recipe, IngredientRating
from .forms import RecipeForm


@login_required
def view_recipe(request, recipe_id):
    """
    Author: Jamie Elder, Victor Smith
    Render page for viewing specific recipe in detail
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, "recipes/recipe_details.html", {"recipe": recipe})


@login_required
def view_all_recipes(request):
    """
    Author: Jamie Elder, Victor Smith
    Render page for viewing all recipes
    """
    recipes = Recipe.objects.all()
    return render(request, "recipes/all_recipes.html", {"recipes": recipes})


def create_recipe(request):
    """
    Author: Jamie Elder, Victor Smith
    Renders the create recipe page, and defines how to process completed create recipe forms.
    """

    ingredient_ratings = IngredientRating.objects.all()
    form = RecipeForm(request.POST or None)
    context = {"form": form, "ingredient_ratings": ingredient_ratings}
    if request.method == "POST":
        if form.is_valid():
            # Get raw data from form
            ingredients = form.cleaned_data.get("ingredients")
            quantities = [
                int(quantity) for quantity in form.cleaned_data.get("quantities")
            ]
            serves = form.cleaned_data.get("serves_num")

            sulphates_score = get_score(ingredients, quantities, serves)

            # from raw ingredients and quantities create comma separated string list of form "<ingredient> - <quantity)g"
            formatted_ingredients = get_ingredients(ingredients, quantities)

            # from raw ingredients create comma separated string list of allergens by searching ingredients database
            formatted_allergens = get_allergens(ingredients)

            # create new recipe entry in database
            new_recipe = Recipe(
                user=request.user,
                recipe_title=form.cleaned_data.get("recipe_title"),
                recipe_ingredients=formatted_ingredients,
                preparation=form.cleaned_data.get("preparation"),
                prep_time=form.cleaned_data.get("prep_time"),
                serves_num=serves,
                sulphates_per_portion=sulphates_score,
                allergens=formatted_allergens,
            )
            new_recipe.save()
            return redirect("recipes:view_all_recipes")
        return render(request, "recipes/create_recipe.html", context)
    else:
        return render(request, "recipes/create_recipe.html", context)


def get_score(ingredients, quantities, serves):
    """
    Author: Jamie Elder
    Calculates the sulphates per portion of a recipe based on the ingredient sulphate score, quantity,
    and number being cooked for.

    # parameter
    ingredients (str[]): A list of the ingredients in the recipe
    quantities (int[]): A list of the quantities of each ingredient in the recipe
    serves (int): The number of people the recipe serves

    # returns
    The amount of emitted sulphates per portion of food
    """
    score = 0
    for i in range(len(ingredients)):
        try:
            ingredient_rating = IngredientRating.objects.get(ingredient=ingredients[i])
            score += ingredient_rating.rating / 1000 * quantities[i] / serves
        except IngredientRating.DoesNotExist:
            continue
    return score


def get_allergens(ingredients):
    """
    Author: Jamie Elder
    Returns the allergens in a list of ingredients, as a comma separated string

    # parameter
    ingredients (str[]): A list of the ingredients in the recipe

    # returns
    The allergens in ingredients as a comma separated string
    """
    formatted_allergens = ""
    for i in range(len(ingredients)):
        if (
            len(IngredientRating.objects.filter(ingredient=ingredients[i])) > 0
            and IngredientRating.objects.get(ingredient=ingredients[i]).allergen != None
        ):
            if formatted_allergens != "":
                formatted_allergens += ", "

            formatted_allergens += IngredientRating.objects.get(
                ingredient=ingredients[i]
            ).allergen
    return formatted_allergens


def get_ingredients(ingredients, quantities):
    """
    Author: Jamie Elder
    Returns a formatted ingredients string with quantities. The string is of the comma separated value type,
    where each value is of the form "<ingredient> - <quantity)g"

    # parameter
    ingredients (str[]): A list of the ingredients in the recipe
    quantities (int[]): A list of the quantities of each ingredient in the recipe

    # returns
    The formatted string of ingredients and quantities
    """
    formatted_ingredients = ""
    for i in range(len(ingredients)):
        formatted_ingredients += ingredients[i] + " - " + str(quantities[i]) + "g"
        if i < len(ingredients) - 1:
            formatted_ingredients += ", "

    return formatted_ingredients
