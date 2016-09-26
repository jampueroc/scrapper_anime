import json
import operator
from collections import OrderedDict

from django.http.response import JsonResponse
from django.views.generic.base import TemplateView

from visualizacion.models.anime import Anime
from visualizacion.models.genre import Genre
from visualizacion.models.licensor import Licensor
from visualizacion.models.producer import Producer
from visualizacion.models.status import Status
from visualizacion.models.studio import Studio
from visualizacion.models.type import Type


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['total_anime'] = Anime.objects.all().count()
        context['total_genres'] = Genre.objects.all().count()
        context['total_licensor'] = Licensor.objects.all().count()
        context['total_producer'] = Producer.objects.all().count()
        context['total_status'] = Status.objects.all().count()
        context['total_studio'] = Studio.objects.all().count()
        context['total_type'] = Type.objects.all().count()
        return context


def genre_percent(request):
    result = dict()
    genres = Genre.objects.all()
    total = Anime.objects.all().count()
    for g in genres:
        anime_genre = Anime.objects.filter(genres=g).count()
        result[g.name] = [1.0*anime_genre/total]
    dict_ordered = OrderedDict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    return JsonResponse( dict_ordered, safe=False)


def get_number_nulls(request):
    result = dict()
    result['name_english'] = Anime.objects.filter(name_english__isnull=True).count()
    result['name_alternatives'] = Anime.objects.filter(name_alternatives__isnull=True).count()
    result['name_japanese'] = Anime.objects.filter(name_japanese__isnull=True).count()
    result['number_episodes'] = Anime.objects.filter(number_episodes__isnull=True).count()
    result['status'] = Anime.objects.filter(status__isnull=True).count()
    result['type'] = Anime.objects.filter(type__isnull=True).count()
    result['aired'] = Anime.objects.filter(aired__isnull=True).count()
    result['producers'] = Anime.objects.filter(producers__isnull=True).count()
    result['licensor'] = Anime.objects.filter(licensor__isnull=True).count()
    result['genres'] = Anime.objects.filter(genres__isnull=True).count()
    result['studios'] = Anime.objects.filter(studios__isnull=True).count()
    result['rating'] = Anime.objects.filter(rating__isnull=True).count()
    result['score'] = Anime.objects.filter(score__isnull=True).count()
    result['ranked'] = Anime.objects.filter(ranked__isnull=True).count()
    result['popularity'] = Anime.objects.filter(popularity__isnull=True).count()
    dict_ordered = OrderedDict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    return JsonResponse( dict_ordered, safe=False)
