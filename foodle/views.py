"""
Author: Jamie Elder, Victor Smith
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

from .models import MealEvent
from recipes.models import Recipe
from users.models import UserProfile
from django.contrib.auth.models import User, Group
from .forms import CreateMealEvent
from .qr import genQrCode
from PIL import Image
import io

from .forms import createGroupForm
from django.contrib.auth.decorators import login_required


def user_in_group(user):
    """
    Author: Jamie Elder
    Check that a user is a member of one and only one group

    # parameters
    user (AbstractUser): The user to be checked

    # returns
    True if the user is a member of exactly one group, False otherwise
    """

    return user.is_authenticated and user.groups.count() == 1


def welcome(request):
    """
    Author: Jamie Elder
    Renders the welcome page
    """
    return render(request, "foodle/welcome.html")


@login_required
def home(request):
    """
    Author: Jamie Elder
    Renders the user home page. Accessible only if logged in.
    """
    return render(request, "foodle/home.html")


@login_required
def play(request):
    """
    Author: Jamie Elder
    Renders the user Foodle game page. Accessible only if logged in. Updates user score with new Foodle ponts.
    """

    # Update the user score when the user caches their points
    if request.method == "POST":
        request.user.userprofile.foodle_score += int(request.POST["score"])
        request.user.userprofile.save()
        return redirect("foodle:home")
    else:
        return render(request, "foodle/foodle.html")


@user_passes_test(user_in_group, login_url="foodle:no_group")
def events(request):
    """
    Author: Jamie Elder
    Renders the view cooking events page. Accessible only if logged in and a member of one group.
    """

    user_group = request.user.groups.first()
    # get all cooking events of the user's group
    cooking_events = MealEvent.objects.filter(group=user_group).order_by("-date_time")
    context = {"cooking_events": cooking_events}
    return render(request, "foodle/events.html", context)


@user_passes_test(user_in_group, login_url="foodle:no_group")
def create_event(request):
    """
    Author: Jamie Elder
    Renders the create cooking event page and handles cooking event creation form submissions.
    Accessible only if logged in and a member of one group.
    """

    if request.method == "POST":
        form = CreateMealEvent(request.POST)
        if form.is_valid():
            event_recipe = Recipe.objects.get(recipe_id=form.cleaned_data.get("recipe"))
            event_group = request.user.groups.first()

            # score = (10 - recipescore/10) * num people
            event_score = max(
                0,
                round(
                    (10 - event_recipe.sulphates_per_portion / 10)
                    * User.objects.filter(groups=event_group).count()
                ),
            )
            new_event = MealEvent(
                user=request.user,
                group=event_group,
                date_time=form.cleaned_data.get("date_time"),
                recipe=event_recipe,
                score=event_score,
            )
            new_event.save()
            return redirect("foodle:events")

    else:
        form = CreateMealEvent()
    return render(request, "foodle/create_event.html", {"form": form})


@login_required
def leaderboard(request):
    """
    Author: Jamie Elder
    Renders the leaderboard page. Accessible only if logged in.
    """
    profiles = list(UserProfile.objects.all())
    profiles.sort(
        reverse=True,
        key=lambda profile: profile.foodle_score
        + profile.env_score,  # combine foodle and recipe scores
    )
    context = {"top_100_profiles": profiles[:100]}
    return render(request, "foodle/leaderboard.html", context)


@user_passes_test(lambda user: user.is_superuser)
def createGroup(request):
    """
    Author: Victor Smith
    Renders the create group page and handle create group form submissions.
    Accessible only to admins.
    """
    all_groups = Group.objects.all()
    if request.method == "POST":
        form = createGroupForm(request.POST or None)
        if form.is_valid():
            form.save()
        return render(request, "foodle/createGroup.html", {"all": all_groups})
    else:
        return render(request, "foodle/createGroup.html", {"all": all_groups})


@user_passes_test(lambda user: user.is_superuser)
def generateQrCode(request):
    """
    Author: Victor Smith
    Renders the generate QR Code page. Accessible only to admins.
    """
    all_groups = Group.objects.all()
    if request.method == "POST":
        newQr = Image.new("RGB", (240, 240), color=(0, 0, 0)) # define QR code image dimensions
        newQr = genQrCode(request.POST["group_name"]) # generate QR link to specific group joining page

        buff = io.BytesIO()
        newQr.save(buff, "jpeg")
        return HttpResponse(buff.getvalue(), content_type="image/jpeg")
    else:
        return render(request, "foodle/generateQrCode.html", {"all": all_groups})


def no_group(request):
    """
    Author: Jamie Elder
    Render redirect page for when user accesses a group only page without a group
    """
    return render(request, "foodle/no_group.html")
