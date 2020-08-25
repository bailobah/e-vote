from django.db import models

# Create your models here.



class Election(models.Model):
    LEGISLATIVE = 2
    PRESIDENTIELLE = 1
    COMMUNALLE = 3
    ELECTION_TYPES = (
        (PRESIDENTIELLE, 'PRESIDENTIELLE'),
        (LEGISLATIVE, 'LEGISLATIVE'),
        (COMMUNALLE, 'COMMUNALLE'),
    )

    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    election_type = models.PositiveSmallIntegerField(choices=ELECTION_TYPES)
    class Meta:
        db_table = "election"
