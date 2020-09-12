import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from locality.models import Locality, LocalitySerializer
from political_party.models import PoliticalParty, PoliticalPartySerializer
from users.models import User, UserSerializer


# Create your models here.

class Election(models.Model):
    LEGISLATIVE = 'LEGISLATIVE'
    PRESIDENTIELLE = 'PRESIDENTIELLE'
    COMMUNALLE = 'COMMUNALLE'
    ELECTION_CHOICES = (
        (PRESIDENTIELLE, 'PRESIDENTIELLE'),
        (LEGISLATIVE, 'LEGISLATIVE'),
        (COMMUNALLE, 'COMMUNALLE'),
    )
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    name = models.CharField(
        max_length=80,
        choices=ELECTION_CHOICES,
        default=PRESIDENTIELLE,
    )
    class Meta:
        db_table = "election"
        ordering = ['-name']
    def __str__(self):
        return '{}'.format(self.name)

class ElectionStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['name']

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "candidate"
    def __str__(self):
        return self.name

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['name','last_name']

class ElectionCandidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False)
    political_party = models.ForeignKey(PoliticalParty,  on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "election_candidate"

class ElectionCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionCandidate
        fields = ['election','candidate','political_party']
        depth = 1

class PollingStation(models.Model):
    name = models.CharField(max_length=100)
    numero = models.IntegerField()
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(default=True)
    adress = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "polling_station"

    def __str__(self):
        return self.name

class PollingStationSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer(many=False, read_only=True)

    class Meta:
        model = PollingStation
        fields = ['name','numero', 'locality']
        #depth=2


def get_pv_path(instance, filename):
    return os.path.join('pvs/{0}/{1}/{2}/{3}'.format(instance.user.id,instance.polling_id,uuid.uuid4(), filename))
def get_incident_path(instance, filename):
    return os.path.join('incident/{0}/{1}/{2}/{3}'.format(instance.user.id,instance.polling_id,uuid.uuid4(), filename))

class Minute(models.Model):
    election = models.ForeignKey(Election, verbose_name=_('Election'), on_delete=models.CASCADE, null=False)
    polling = models.ForeignKey(PollingStation, verbose_name=_('Numero du bureau de vote'), on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User,verbose_name=_('Centralisateur'), on_delete=models.CASCADE, null=False)
    nbr_registrants = models.IntegerField(_('Nombre d\'inscrits'), blank=False, null=False)
    nbr_voters = models.IntegerField(_('Nombre de votants'),blank=False, null=False)
    nbr_invalids_ballots = models.IntegerField(_('Total des bulletins nuls'),blank=False, null=False)
    nbr_votes_cast = models.IntegerField(_('Suffrage valablement exprimé'), blank=False, null=False)
    image = models.FileField(_('Photo du PV'),
                             upload_to= get_pv_path,
                             blank=False,
                             null=False
                             )
    incident = models.BooleanField(default=False)
    comment = models.TextField()
    file = models.FileField(_('Photo de l\'incident'),
                     upload_to=get_incident_path,
                     blank=False,
                     null=False
                     )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "minute"
        ordering = ['-id']

class MinuteDetails(models.Model):
    minute = models.ForeignKey(Minute, on_delete=models.CASCADE, null=False)
    political_party = models.ForeignKey(PoliticalParty, on_delete=models.CASCADE, null=False)
    nbr_votes_obtained = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=100)


    class Meta:
        db_table = "minute_details"

class MinuteDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MinuteDetails
        fields = ['political_party','nbr_votes_obtained']


class MinuteSerializer(serializers.ModelSerializer):
    minute_details = MinuteDetailsSerializer(many=True)

    class Meta:
        model = Minute
        fields = ['election','polling','user','nbr_registrants', 'nbr_votes_cast','nbr_voters', 'nbr_invalids_ballots','image','minute_details']

    def create(self, validated_data):

        minute_details = validated_data.pop('minute_details')

        minute = Minute.objects.create(**validated_data)
        for minute_detail in minute_details:
            print(minute_details)
            MinuteDetails.objects.create(minute=minute, **minute_detail)
        return minute




