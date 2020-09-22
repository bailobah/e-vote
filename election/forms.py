from django import forms
from django.forms import inlineformset_factory

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

    image = forms.ImageField(widget=forms.FileInput(attrs={'type': 'file', 'class':'custom-file'}), label = "Joindre le PV",)
    file = forms.ImageField(widget=forms.FileInput(attrs={'type': 'file', 'class':'custom-file'}), label = "Joindre la photo",)

    class Meta:
        model = Minute
        exclude = ['updated_at','created_at',]

    def __init__(self, user, *args, **kwargs):

        super(MinuteForm, self).__init__(*args, **kwargs)
        self.user = user
        localitys = Allocation.objects.filter(user=self.user).values('locality_id')
        self.fields['polling'].queryset = PollingStation.objects.filter(locality__in=localitys).filter(is_active=True)
        # self.fields['election'].queryset  = Election.objects.filter(pk=localitys)
        self.fields['election'].widget = forms.widgets.HiddenInput()
        self.fields['user'].widget = forms.widgets.HiddenInput()
        self.fields['nbr_votes_cast'].widget = forms.widgets.HiddenInput()

class MinuteUpdateForm(forms.ModelForm):

    image = forms.ImageField(widget=forms.FileInput(attrs={'type': 'file', 'class':'custom-file'}), label = "Joindre le PV", required=False)
    file = forms.ImageField(widget=forms.FileInput(attrs={'type': 'file', 'class':'custom-file'}), label = "Joindre la photo",required=False)

    class Meta:
        model = Minute
        exclude = ['updated_at','created_at',]

class MinuteDetailForm(forms.ModelForm):
    class Meta:
        model = MinuteDetails
        exclude = ['description',]

MinuteDetailsFormset = inlineformset_factory(
    Minute, MinuteDetails, form = MinuteDetailForm, extra=1, max_num=11,can_delete=True
)

