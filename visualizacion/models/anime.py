from django.core.cache import cache
from django.db import models


class Anime(models.Model):
    name_english = models.ForeignKey('Title', related_name='anime_name_english', null=True)
    name_alternatives = models.ManyToManyField('Title', related_name='anime_others_names')
    name_japanese = models.CharField(max_length=255, null=True)
    number_episodes = models.IntegerField(null=True)
    status = models.CharField(max_length=255, null=True)
    type = models.ForeignKey('Type', null=True, related_name='anime_type')
    aired = models.DateField(null=True)
    producers = models.ManyToManyField('Producer', related_name='anime_producer')
    licensor = models.ManyToManyField('Licensor', related_name='anime_licensors')
    genres = models.ManyToManyField('Genre', related_name='anime_genres')
    studios = models.ManyToManyField('Studio', related_name='anime_studio')
    rating = models.CharField(max_length=255)
    score = models.FloatField(null=True)
    ranked = models.IntegerField(null=True)
    popularity = models.IntegerField(null=True)
    url = models.TextField(unique=True)

    def __unicode__(self):
        if self.name_english:
            return unicode(self.name_english)
        if len(self.name_alternatives.all()) >0:
            return unicode(self.name_alternatives.all()[0])
        if self.name_japanese:
            return unicode(self.name_japanese)

        return "no title"

    def get_genres_pretty(self):
        id = self.id
        result = ""
        name = "g"+str(id)
        in_cache = cache.get(name)
        if in_cache:
            result = in_cache
        else:
            g = [str(g) for g in self.genres.all()]
            result = ", ".join(g)
            cache.set(name, result)
        return result

    def get_producers_pretty(self):
        id = self.id
        result = ""
        name = "p" + str(id)
        in_cache = cache.get(name)
        if in_cache:
            result = in_cache
        else:
            p = [str(p) for p in self.producers.all()]
            result = ", ".join(p)
            cache.set(name, result)
        return result
