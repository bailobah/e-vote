from django import forms
from .models import LocalityType


class LocalityTypeForm(forms.ModelForm):
    class Meta:
        model = LocalityType
        fields = ('name',  'is_active','description')