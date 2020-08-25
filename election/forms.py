from django import forms
from election.models import Election


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ('id', 'description', 'is_active', 'election_type')