import urllib
from datetime import datetime

from django.db import models

# Create your models here.
from django.forms import ModelForm

from locality.models import Locality
from political_party.models import PoliticalParty
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.core.files import File
import os
from utils import utils

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


class ElectionCandidate(models.Model):
    election = models.ForeignKey(Election,  on_delete=models.CASCADE, null=False)
    candidate = models.ForeignKey(Candidate,  on_delete=models.CASCADE, null=False)
    political_party = models.ForeignKey(PoliticalParty,  on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "election_candidate"

class PollingStation(models.Model):
    name = models.CharField(max_length=100)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(default=True)
    adress = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "polling_station"

    def __str__(self):
        return self.name

def user_directory_path(instance):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}'.format(instance.user.id)

class Minute(models.Model):
    election = models.ForeignKey(Election, verbose_name=_('Election'), on_delete=models.CASCADE, null=False)
    polling = models.ForeignKey(PollingStation, verbose_name=_('Numero du bureau de vote'), on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User,verbose_name=_('Centralisateur'), on_delete=models.CASCADE, null=False)
    nbr_registrants = models.IntegerField(_('Nombre d\'inscrits'), blank=False, null=False)
    #nbr_polling_planned = models.IntegerField(_('Nombre de bureau de vote'), blank=False, null=True)
    #nbr_polling_real = models.IntegerField(blank=True, null=True)
    nbr_voters = models.IntegerField(_('Nombre de votants'),blank=False, null=False)
    nbr_invalids_ballots = models.IntegerField(_('Total des bulletins nuls'),blank=False, null=False)
    nbr_votes_cast = models.IntegerField(_('Suffrage valablement exprimé'), blank=False, null=False)
    image_file = models.ImageField(_('Photo du PV'),upload_to=user_directory_path,blank=False, null=False)
    #image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "minute"

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            self.image_file.save(
                os.path.basename(self.image_url),
                File(open(result[0]))
            )
            self.save()


class MinuteDetails(models.Model):
    id_polling = models.ForeignKey(PollingStation,  on_delete=models.CASCADE, null=False)
    id_political_party = models.ForeignKey(PoliticalParty,  on_delete=models.CASCADE, null=False)
    nbr_votes_obtained = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = "minute_details"

