from django import forms

from election.models import Election, Minute, PollingStation, MinuteDetails
from locality.models import Allocation


class ElectionForm(forms.ModelForm):

    class Meta:
        model = Election
        fields = ('id', 'description', 'is_active', 'name')

class MinuteUpdateForm(forms.ModelForm):

    class Meta:
        model = Minute
        fields = '__all__'
        exclude = ['updated_at','image']
        forms.HiddenInput()

class MinuteForm(forms.ModelForm):

    election = forms.IntegerField(required=False, widget = forms.widgets.HiddenInput())
    user = forms.IntegerField(required=False, widget = forms.widgets.HiddenInput())

    class Meta:
        model = Minute
        fields = '__all__'
        exclude = ['updated_at']
        forms.HiddenInput()

class MinuteFormFilterForm(forms.ModelForm):
    election = forms.IntegerField(required=False)
    user = forms.IntegerField(required=False)
    class Meta:
        model = Minute
        exclude = ['updated_at','created_at']

    def __init__(self, user, *args, **kwargs):
        super(MinuteFormFilterForm, self).__init__(*args, **kwargs)
        localitys = Allocation.objects.filter(user=user).values('locality_id')
        self.fields['polling'].queryset  = PollingStation.objects.filter(locality__in=localitys).filter(is_active=True)
        #self.fields['election'].queryset  = Election.objects.filter(pk=localitys)
        self.fields['election'].widget = forms.widgets.HiddenInput()
        self.fields['user'].widget = forms.widgets.HiddenInput()

class MinuteDetailsForm(forms.ModelForm):

    class Meta:
        model = MinuteDetails
        exclude = ['updated_at','created_at']