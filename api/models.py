from django.db import models

from django.utils.translation import gettext_lazy as _
# Create your models here.
from rest_framework import serializers

from election.models import Election, PollingStation, PollingStationSerializer, GetMinuteDetailsSerializer
from political_party.models import PoliticalParty, PoliticalPartySerializer
from users.models import User, UserSerializer


class MinuteSms(models.Model):
    election = models.ForeignKey(Election, verbose_name=_('Election'), on_delete=models.CASCADE, null=False)
    polling = models.ForeignKey(PollingStation, verbose_name=_('Bureau de vote'), on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, verbose_name=_('Centralisateur'), on_delete=models.CASCADE, null=False)
    nbr_registrants = models.IntegerField(_('Nombre d\'inscrits'), blank=True, null=False)
    nbr_voters = models.IntegerField(_('Nombre de votants'),blank=False, null=False)
    nbr_invalids_ballots = models.IntegerField(_('Bulletins nuls'),blank=False, null=False)
    nbr_votes_cast = models.IntegerField(_('Suffrage valablement exprimé'), blank=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "minute_sms"
        ordering = ['-id']

class MinuteDetailsSms(models.Model):
    minute = models.ForeignKey(MinuteSms, on_delete=models.CASCADE, null=False)
    political_party = models.ForeignKey(PoliticalParty, on_delete=models.CASCADE, null=False, verbose_name=_('Parti'))
    nbr_votes_obtained = models.IntegerField(blank=False, null=False,  verbose_name=_('Votes obtenues'))

    class Meta:
        db_table = "minute_details_sms"


class GetMinuteDetailsSmsSerializer(serializers.ModelSerializer):
    political_party = PoliticalPartySerializer()

    class Meta:
        model = MinuteDetailsSms
        fields = ['political_party','nbr_votes_obtained']
        depth = 1


class GetMinuteSmsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    polling = PollingStationSerializer()
    minute_details = GetMinuteDetailsSmsSerializer(many=True, source='minutedetailssms_set')

    class Meta:
        model = MinuteSms
        fields = ['id', 'polling', 'user', 'nbr_registrants', 'nbr_votes_cast', 'nbr_voters','nbr_invalids_ballots','minute_details']

class RejectedSms(models.Model):
    sms =  models.CharField(max_length=1000, default="")
    sender_phone = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    errorMessage = models.CharField(max_length=1000, default="")
    delegate_phone = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "rejected_sms"

