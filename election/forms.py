from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.forms import TextInput, inlineformset_factory
from django.utils.translation import gettext_lazy as _
from election.models import Election, Minute, PollingStation, MinuteDetails
from locality.models import Allocation

from .custom_layout_object import *
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
    # election = forms.IntegerField(required=False, widget=forms.widgets.HiddenInput())
    # user = forms.IntegerField(required=False, widget=forms.widgets.HiddenInput())

    class Meta:
        model = Minute
        exclude = ['updated_at','created_at',]

    def __init__(self, user, *args, **kwargs):

        super(MinuteForm, self).__init__(*args, **kwargs)
        self.user = user #kwargs.pop('user', None)
        print("========================")
        print(self.user)
        localitys = Allocation.objects.filter(user=self.user).values('locality_id')
        self.fields['polling'].queryset = PollingStation.objects.filter(locality__in=localitys).filter(is_active=True)
        # self.fields['election'].queryset  = Election.objects.filter(pk=localitys)
        self.fields['election'].widget = forms.widgets.HiddenInput()
        self.fields['user'].widget = forms.widgets.HiddenInput()
        self.fields['nbr_votes_cast'].widget = forms.widgets.HiddenInput()




class MinuteDetailForm(forms.ModelForm):
    class Meta:
        model = MinuteDetails
        exclude = ['description',]


MinuteDetailsFormset = inlineformset_factory(
    Minute, MinuteDetails, form=MinuteDetailForm, extra=1, max_num=3,can_delete=True
)

