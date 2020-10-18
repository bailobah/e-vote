from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['phone_number','last_name','first_name', 'is_staff','is_superviser']
