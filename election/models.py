import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

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
    adress = models.CharField(max_length=100, default="")
    nbr_registrants = models.IntegerField(blank=True)

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

def get_pv_path(instance, filename):
    return os.path.join('pvs/{0}/{1}/{2}/{3}'.format(instance.user.id,instance.polling_id,uuid.uuid4(), filename))
def get_incident_path(instance, filename):
    return os.path.join('incident/{0}/{1}/{2}/{3}'.format(instance.user.id,instance.polling_id,uuid.uuid4(), filename))

class Minute(models.Model):
    election = models.ForeignKey(Election, verbose_name=_('Election'), on_delete=models.CASCADE, null=False)
    polling = models.ForeignKey(PollingStation, verbose_name=_('Bureau de vote'), on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, verbose_name=_('Centralisateur'), on_delete=models.CASCADE, null=False)
    nbr_registrants = models.IntegerField(_('Nombre d\'inscrits'), blank=True, null=False)
    nbr_voters = models.IntegerField(_('Nombre de votants'),blank=False, null=False)
    nbr_invalids_ballots = models.IntegerField(_('Bulletins nuls'),blank=False, null=False)
    nbr_votes_cast = models.IntegerField(_('Suffrage valablement exprimé'), blank=True, null=False)
    nbr_votes_pro = models.IntegerField(_('Nombre de vote par procuration'), default=0)

    image = models.FileField(_('Photo du PV'),
                             upload_to= get_pv_path,
                             blank=True,
                             null=False
                             )
    incident = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    file = models.FileField(_('Photo de l\'incident'),
                            upload_to=get_incident_path,
                            blank=True,
                            null=False
                            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "minute"
        ordering = ['-id']

class MinuteDetails(models.Model):
    minute = models.ForeignKey(Minute, on_delete=models.CASCADE, null=False)
    political_party = models.ForeignKey(PoliticalParty, on_delete=models.CASCADE, null=False, verbose_name=_('Parti'))
    nbr_votes_obtained = models.IntegerField(blank=False, null=False,  verbose_name=_('Votes obtenues'))

    class Meta:
        db_table = "minute_details"

class MinuteDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MinuteDetails
        fields = ['political_party','nbr_votes_obtained']

class GetMinuteDetailsSerializer(serializers.ModelSerializer):
    political_party = PoliticalPartySerializer()
    class Meta:
        model = MinuteDetails
        fields = ['political_party','nbr_votes_obtained']
        depth = 1
class GetMinuteSerializer(serializers.ModelSerializer):
    minute_details = GetMinuteDetailsSerializer(many=True, source='minutedetails_set')

    class Meta:
        model = Minute
        fields = ['id','polling','user','nbr_registrants', 'nbr_votes_cast','nbr_voters', 'nbr_invalids_ballots','image','incident','comment','file','minute_details']
        #depth = 1
class MinuteSerializer(serializers.ModelSerializer):
    minute_details = MinuteDetailsSerializer(many=True)

    class Meta:
        model = Minute
        fields = ['id','polling','user','nbr_registrants', 'nbr_votes_cast','nbr_voters', 'nbr_invalids_ballots','image','incident','comment','file','minute_details']

    def create(self, validated_data):

        minute_details = validated_data.pop('minute_details')

        nbr_votes_cast = int(validated_data['nbr_voters']) - int(validated_data['nbr_invalids_ballots'])
        nbr_votes_obtaineds = list(map(lambda x: x['nbr_votes_obtained'], minute_details))
        if(nbr_votes_cast != sum(nbr_votes_obtaineds)):
            raise ValidationError({'nbr_votes_obtained': f'Total des votes obtenue ({sum(nbr_votes_obtaineds)}) doit etre egal au nombre de vote valide ({nbr_votes_cast})'})
        validated_data['election'] = get_object_or_404(Election, pk=1)
        validated_data['nbr_votes_cast'] = nbr_votes_cast
        #validated_data['nbr_registrants'] = 500

        minute = Minute.objects.create(**validated_data)
        for minute_detail in minute_details:
            MinuteDetails.objects.create(minute=minute, **minute_detail)

        ps = PollingStation.objects.get(id=minute.polling_id)
        ps.is_active = False
        ps.save()
        return minute

    def update(self, instance, validated_data):
        print(instance)

        # datail_data = validated_data.pop('minute_details')
        # print(datail_data)
        # print(datail_data)
        # details = (instance.minute_details).all()
        # print(details)
        # albums = list(details)
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.instrument = validated_data.get('instrument', instance.instrument)
        # instance.save()
        #
        # for album_data in datail_data:
        #     album = albums.pop(0)
        #     album.name = album_data.get('name', album.name)
        #     album.release_date = album_data.get('release_date', album.release_date)
        #     album.num_stars = album_data.get('num_stars', album.num_stars)
        #     album.save()
        return instance

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #
    #     quiz_data = validated_data.get('quiz')
    #     if quiz_data:
    #         instance.quiz_set.clear()
    #         Quiz.objects.bulk_create(
    #             [
    #                 Quiz(module_referred=instance, **quiz)
    #                 for quiz in quiz_data
    #             ],
    #         )
    #     instance.save()
    #     return instance





