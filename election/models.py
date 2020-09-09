import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from locality.models import Locality, LocalitySerializer
from political_party.models import PoliticalParty
from users.models import User

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "minute"
        ordering = ['-id']

class MinuteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        Minute.objects.create(**validated_data)

    class Meta:
        model = Minute
        fields = ['nbr_registrants', 'nbr_voters', 'nbr_invalids_ballots']

class MinuteDetails(models.Model):
    polling = models.ForeignKey(PollingStation, on_delete=models.CASCADE, null=False)
    id_political_party = models.ForeignKey(PoliticalParty, on_delete=models.CASCADE, null=False)
    nbr_votes_obtained = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = "minute_details"

