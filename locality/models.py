from django.db import models

# Create your models here.
from rest_framework import serializers

from locality_type.models import LocalityType, LocalityTypeSerializer
from users.models import User

class Locality(models.Model):
    name = models.CharField(max_length=100)
    locality_type = models.ForeignKey(LocalityType, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "locality"
        #fields = ['name', 'locality_type', 'description']
    def __str__(self):
        return self.name

class LocalitySerializer(serializers.ModelSerializer):
    locality_type = LocalityTypeSerializer(many=False, read_only=True)
    class Meta:
        model = Locality
        fields = ['name', 'locality_type', 'description']
        depth = 1

class SectorisationLocality(models.Model):
    locality_inf = models.ForeignKey(Locality, related_name='id_locality_inf', on_delete=models.CASCADE, null=False)
    locality_sup = models.ForeignKey(Locality, related_name='id_locality_sup', on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sectorisation_locality"

class Allocation(models.Model):
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "allocation"
    # def __str__(self):
    #     return f' {self.id}, {self.user.last_name} {self.user.first_name}, ville ({self.locality.name})'


class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = ['description']
