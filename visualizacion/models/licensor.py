from django.db import models


class Licensor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
