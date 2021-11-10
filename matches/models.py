from django.db import models

# Create your models here.
class Match(models.Model):
    sport = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    ligue = models.CharField(max_length=200)
    name  = models.CharField(max_length=200)
    time  = models.CharField(max_length=200)
    sport = models.CharField(max_length=200)

    homeOdds = models.CharField(max_length=200)
    xOdds    = models.CharField(max_length=200)
    awayOdds = models.CharField(max_length=200)

    def __str__(self):
        return self.name