from django import forms
from api.models import RejectedSms


class RejectedSmsForm(forms.ModelForm):
    class Meta:
        model = RejectedSms
        fields = '__all__'