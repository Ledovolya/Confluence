from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import db.models

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=130, required=True)
    last_name = forms.CharField(max_length=130, required=True)
    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "password1", "password2", "email")
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class page_form(forms.Form):
    command = forms.CharField(required=False)
    id = forms.CharField(required=False)
    user = forms.CharField(required=False)
    password = forms.CharField(required=False)
    space = forms.CharField(required=False)
    title = forms.CharField(required=False)
    text = forms.CharField(required=False)