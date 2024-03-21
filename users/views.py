"""
Author: Jamie Elder
"""

from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserDeletionForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def register(request):
    """
    Author: Jamie Elder
    Render the registration page and pass registration form submissions
    to be handles by the built in handler.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)

@login_required
def join_group(request, group_name):
    """
    Author: Jamie Elder
    Render the join group page, and adds a user to the requested group.
    Accessible only to logged in users
    """

    # check if group exists
    try:
        to_join = Group.objects.get(name = group_name)
    except Group.DoesNotExist:
        return HttpResponse("The group you are trying to join does not exist")
    
    if (request.GET.get('leave_group_btn')):
        # remove the user from all current groups if they request. Can only be a member of one group.
        for g in request.user.groups.all():
            g.user_set.remove(request.user)
    
    # Add users to their requested group and redirect to home
    if (request.user.groups.count() == 0):
        to_join.user_set.add(request.user)
        return redirect('foodle:home')
    else:
        # if user is already a member of group, allow them to leave
        return render(request,'users/leave_group.html')
    
@login_required
def delete_user(request):
    """
    Author: Jamie Elder
    Renders acount deletion page and handles account deletion requests. Accessible only to logged in users. 
    """
    if request.method == 'POST':
        delete_form = UserDeletionForm(request.POST, instance=request.user)
        user = request.user
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('foodle:welcome')
    else:
        delete_form = UserDeletionForm(instance=request.user)

    context = {
        'delete_form': delete_form
    }

    return render(request, 'users/delete_account.html', context)

def terms(request):
    """
    Author: Jamie Elder
    Renders the terms and conditions page.
    """
    return render(request, 'users/terms.html')