from django.db import models
from constellations.models import Constellation


class Star(models.Model):
    name = models.CharField(max_length=100)
    constellation = models.ForeignKey(
        Constellation,
        on_delete=models.CASCADE,
        related_name='stars'
    )
    ra = models.FloatField(help_text="Right Ascension (도 단위)")
    dec = models.FloatField(help_text="Declination (도 단위)")

    magnitude = models.FloatField(help_text="시등급 (밝기)", null=True, blank=True)
    spectral_type = models.CharField(max_length=10, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)

    is_custom = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.constellation.name})"
