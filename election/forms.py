from pathlib import Path

from django import forms
from django.forms.widgets import FileInput

from election.models import Election, Minute, PollingStation
from locality.models import Allocation, Locality
from users.models import User


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ('id', 'description', 'is_active', 'name')

class MinuteUpdateForm(forms.ModelForm):

    class Meta:
        model = Minute
        fields = '__all__'
        exclude = ['updated_at','image_file']
        forms.HiddenInput()

class MinuteForm(forms.ModelForm):
    election = forms.IntegerField(required=False, widget = forms.widgets.HiddenInput())
    user = forms.IntegerField(required=False, widget = forms.widgets.HiddenInput())


    class Meta:
        model = Minute
        fields = '__all__'
        exclude = ['updated_at','image_file']
        forms.HiddenInput()

class MinuteFormFilterForm(forms.ModelForm):
    election = forms.IntegerField(required=False)
    user = forms.IntegerField(required=False)
    class Meta:
        model = Minute
        exclude = ['updated_at','created_at','image_url']

    def __init__(self, user, *args, **kwargs):
        super(MinuteFormFilterForm, self).__init__(*args, **kwargs)
        localitys = Allocation.objects.filter(user=user).values('locality_id')
        self.fields['polling'].queryset  = PollingStation.objects.filter(locality__in=localitys)
        #self.fields['election'].queryset  = Election.objects.filter(pk=localitys)
        self.fields['election'].widget = forms.widgets.HiddenInput()
        self.fields['user'].widget = forms.widgets.HiddenInput()
