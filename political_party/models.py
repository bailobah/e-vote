from django.db import models

# Create your models here.

from rest_framework import serializers

class PoliticalParty(models.Model):

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "political_party"
        #ordering = ['name', ]

    def __str__(self):
        return self.name

class PoliticalPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = ['name', 'description', ]

