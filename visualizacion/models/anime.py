from django.db import models


class Anime(models.Model):
    name_english = models.ForeignKey('Title', related_name='anime_name_english', null=True)
    name_alternatives = models.ManyToManyField('Title', related_name='anime_others_names')
    name_japanese = models.ForeignKey('Title', related_name='anime_name_japanese', null=True)
    number_episodes = models.IntegerField(null=True)
    status = models.ForeignKey('Status', null=True, related_name='anime_status')
    type = models.ForeignKey('Type', null=True, related_name='anime_type')
    aired = models.DateField(null=True)
    producers = models.ManyToManyField('Producer', related_name='anime_producer')
    license = models.ForeignKey('License', null=True, related_name='anime_studio')
    genres = models.ManyToManyField('Genre', related_name='anime_genres')
    studios = models.ForeignKey('Studio', null=True, related_name='anime_studio')
    rating = models.CharField(max_length=255)
    score = models.FloatField(null=True)
    ranked = models.IntegerField(null=True)
    popularity = models.IntegerField(null=True)
    url = models.TextField(unique=True)

    def __unicode__(self):
        if self.name_english:
            return unicode(self.name_english)
        if self.name_japanese:
            return unicode(self.name_japanese)
        elif len(self.name_alternatives.all()) >0:
            return unicode(self.name_alternatives.all()[0])
        else:
            return "no title"
