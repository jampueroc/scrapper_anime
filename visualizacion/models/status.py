from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
