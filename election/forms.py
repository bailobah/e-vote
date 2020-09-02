from pathlib import Path

from django import forms
from election.models import Election,Minute
from locality.models import Allocation
from users.models import User


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ('id', 'description', 'is_active', 'name')


class MinuteForm(forms.ModelForm):
    image_file = forms.ImageField(
        label='Select a PV',
    )

    def clean_user_file(self, *args, **kwargs):
        cleaned_data = super(MinuteForm,self).clean()
        image_file = cleaned_data.get("image_file")
        if image_file:
            if image_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File is too big.")
            if not Path(image_file).suffix.strip().lower() in ['.jpg','.png','.gif','.jpeg']:
                raise forms.ValidationError("File does not look like as picture.")
        return image_file

    class Meta:
        model = Minute
        fields = ('election','polling','user','nbr_polling_planned','nbr_polling_real','nbr_registrants','nbr_voters','nbr_invalids_ballots','nbr_votes_cast','image_file')

class MinuteFormFilterForm(forms.ModelForm):
    class Meta:
        model = Minute
        exclude = ['updated_at','created_at','image_url']

    def __init__(self, user, *args, **kwargs):
        super(MinuteFormFilterForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = Allocation.objects.filter(user=user)
        #self.fields['locality'].queryset = Allocation.objects.filter(user=user.pk)


