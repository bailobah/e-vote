from django import forms
from political_party.models import PoliticalParty


class PoliticalPartyForm(forms.ModelForm):
    class Meta:
        model = PoliticalParty
        fields = ('name',  'is_active','description')