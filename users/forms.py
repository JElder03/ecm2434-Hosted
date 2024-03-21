"""
Author: Jamie Elder
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
    """
    Extends the base user creation form to include emails and ensure the user has agreed to the T&Cs.
    """
    email = forms.EmailField(required=True)
    terms_confirmed = forms.BooleanField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",'terms_confirmed')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserDeletionForm(forms.ModelForm):
    """
    Form for submitting a request to delete your user profile.
    """
    class Meta:
        model = User
        fields = []   #Form has only submit button.