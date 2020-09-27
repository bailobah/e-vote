from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, Profile


class UserUpdateForm(forms.ModelForm):

    last_name = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    class Meta:
        model = User
        fields = ['phone_number','last_name','first_name']

class ProfileUpdateForm(forms.ModelForm):

    birth_date = forms.DateField()
    image = forms.ImageField()
    about = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    country = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    code_postal = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = Profile
        fields = ['birth_date','image','about', 'country', 'code_postal']

