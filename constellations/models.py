from django.db import models


class Constellation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    connections = models.JSONField(
        null=True, blank=True, help_text="별들 간 연결 (Star ID 쌍 목록)")

    def __str__(self):
        return self.name
