from django.db import models


class Title(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)
