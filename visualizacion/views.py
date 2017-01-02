import json
import operator
from collections import OrderedDict

import datetime

from django.core.cache import cache
from django.db.models.aggregates import Count
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

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


class TryingD3(IndexView):
    template_name = 'try_d3.html'


class GenreDetail(DetailView):
    model = Genre
    template_name = 'genre_detail.html'



def genre_percent(request):
    result = []
    genres = Genre.objects.all()
    total = Anime.objects.all().count()
    for g in genres:
        anime_genre = Anime.objects.filter(genres=g).count()
        anime = dict()
        anime['name'] = g.name
        anime['value'] = 1.0*anime_genre/total
        anime['total'] = anime_genre
        anime['id'] = g.id
        result.append(anime)
    return JsonResponse(result, safe=False)


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


@cache_page(60 * 15, key_prefix="json_producers")
def get_genres_by_producers(request):
    result = dict()
    producers = Producer.objects.all()
    genres = Genre.objects.all()
    total = Anime.objects.all().count()
    for p in producers:
        list_p = list()
        for g in genres:
            list_p.append(Anime.objects.filter(producers=p,genres=g).count())
        result[p.name] = list_p
    dict_result= {
        'producers':result,
        'categories': [g.name for g in genres]
    }
    return JsonResponse(dict_result, safe=False)


def great_producers(request):
    genres = Genre.objects.all()
    producers = Producer.objects.all()
    list_results = list()
    for g in genres:
        for p in producers:
            result = dict()
            gen_prod_count= Anime.objects.filter(genres=g, producers=p).count()
            result['genre']= g.name
            result['producer']= p.name
            result['production']= gen_prod_count
            list_results.append(result)
    return JsonResponse(list_results, safe=False)


def anual_genres_ranking(request):
    genres = Genre.objects.all()
    start_year = 1980
    generation_gap= 1
    year= start_year + generation_gap
    list_results = list()
    while year > start_year and year < 2017:
        for g in genres:
            result = dict()
            gen_count= Anime.objects.filter(genres=g,aired__year=year).count() #add filter of date
            result['year']= year
            result['production']= gen_count
            result['genre']= g.name
            list_results.append(result)
        year= year + generation_gap
    return JsonResponse( list_results, safe=False)


def anual_genres_battle(request):
    genres = Genre.objects.all()
    start_year = 1980
    generation_gap= 1
    year= start_year + generation_gap
    list_results = list()
    while year > start_year and year < 2017:
        result = dict()
        shounen_count= Anime.objects.filter(genres__name="Shounen",aired__year=year).count() #add filter of date
        shoujo_count= Anime.objects.filter(genres__name="Shoujo",aired__year=year).count() #add filter of date
        ecchi_count= Anime.objects.filter(genres__name="Ecchi",aired__year=year).count() #add filter of date
        hentai_count= Anime.objects.filter(genres__name="Hentai",aired__year=year).count() #add filter of date
        yaoi_count= Anime.objects.filter(genres__name="Yaoi",aired__year=year).count() #add filter of date
        yuri_count= Anime.objects.filter(genres__name="Yuri",aired__year=year).count() #add filter of date
        result['year']= year
        result['shounen']= shounen_count
        result['shoujo']= shoujo_count
        result['ecchi']= ecchi_count
        result['hentai']= hentai_count
        result['yaoi']= yaoi_count
        result['yuri']= yuri_count
        list_results.append(result)
        year= year + generation_gap
    return JsonResponse( list_results, safe=False)


class FinalVersionView(TemplateView):
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context = super(FinalVersionView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all().order_by('name')
        context['producers'] = Producer.objects.all().order_by('name')
        positions = Anime.objects.values('genres__name').annotate(dcount=Count('*')).order_by('-dcount')
        context['ranking'] = { p['genres__name']: index+1 for index, p in enumerate(positions)}
        positions = Anime.objects.values('producers__name').annotate(dcount=Count('*')).order_by('-dcount')
        context['ranking_producers'] = { p['producers__name']: index+1 for index, p in enumerate(positions)}
        return context


def anime_list(request):
    in_cache = cache.get('data_anime')
    if in_cache:
        result = in_cache
    else:
        animes = Anime.objects.all()
        result =list()
        for a in animes:
            result.append([str(a),
                           a.get_genres_pretty(),
                           a.get_producers_pretty(),
                           a.aired,
                           a.url
                           ])
        cache.set('data_anime', result)
    return JsonResponse({'data':result},safe=False)

class GenreDataView(DetailView):
    model = Genre

    def get(self, request, *args, **kwargs):
        result = Anime.objects.filter(
            genres=self.get_object()
        ).values(
            'producers','producers__name'
        ).annotate(dcount=Count('producers')).order_by('-dcount')[:5]
        return JsonResponse(list(result),safe=False)


class ProducerDataView(DetailView):
    model = Producer

    def get(self, request, *args, **kwargs):
        result = Anime.objects.filter(
            producers=self.get_object()
        ).values(
            'genres', 'genres__name'
        ).annotate(dcount=Count('genres')).order_by('-dcount')[:5]
        return JsonResponse(list(result), safe=False)


class GenreDataGraphView(DetailView):
    model = Genre

    def get(self, request, *args, **kwargs):
        result = Anime.objects.filter(
            genres=self.get_object(), aired__isnull=False
        ).extra(select={'year': "EXTRACT(year FROM aired)"}).values('year').annotate(producciones=Count('*')).order_by('year')
        i = 1
        list_result = []
        list_result.append(result[0])
        last = result[0]
        while  last['year']<result[len(result)-1]['year']:
            current = result[i]
            if current['year']-1 != last['year']:
                last = {
                    'year': last['year']+1,
                    'producciones': 0
                }
            else:
                last = current
                i+=1
            list_result.append(last)
        return JsonResponse(list_result, safe=False)


class ProducerDataGraphView(DetailView):
    model = Producer

    def get(self, request, *args, **kwargs):
        result = Anime.objects.filter(
            producers=self.get_object(), aired__isnull=False
        ).extra(select={'year': "EXTRACT(year FROM aired)"}).values('year').annotate(producciones=Count('*')).order_by('year')
        i = 1
        list_result = []
        list_result.append(result[0])
        last = result[0]
        while last['year']<result[len(result)-1]['year']:
            current = result[i]
            if current['year']-1 != last['year']:
                last = {
                    'year': last['year']+1,
                    'producciones': 0
                }
            else:
                last = current
                i+=1
            list_result.append(last)
        return JsonResponse(list_result, safe=False)


class VersusGraphView(TemplateView):

    def get(self, request, *args, **kwargs):
        g1 = int(request.GET.get('g1'))
        g2 = int(request.GET.get('g2'))
        g1_result = Anime.objects.filter(
             aired__isnull=False, genres__pk=g1
        ).extra(select={'year': "EXTRACT(year FROM aired)"}).values('genres','year').annotate(dcount=Count('*')).order_by('year')
        g2_result = Anime.objects.filter(
             aired__isnull=False, genres__pk=g2
        ).extra(select={'year': "EXTRACT(year FROM aired)"}).values('genres','year').annotate(dcount=Count('*')).order_by('year')
        i = 1
        list_years = []
        years_query = Anime.objects.filter(genres__pk__in=[g1,g2]).extra(select={'year': "EXTRACT(year FROM aired)"}).values('year').distinct().order_by('year')
        last = None
        for item in years_query:
            if item['year'] is not None:
                if last is None:
                    last = item['year']
                elif last+1 != item['year']:
                    while last+1 != item['year']:
                        last +=1
                        list_years.append(last)
                list_years.append(item['year'])
                last = item['year']
        i = 0
        j =0
        list_g1 = []
        g1_name= Genre.objects.get(id=g1).name
        # import ipdb; ipdb.set_trace()
        while i<len(list_years) :
            if j<len(g1_result) and g1_result[j]['year'] is not None:
                if g1_result[j]['year'] == list_years[i]:
                    list_g1.append(g1_result[j]['dcount'])
                    j += 1
                    i += 1
                else:
                    while g1_result[j]['year'] > list_years[i]:
                        i+=1
                        list_g1.append(0)


            else:
                list_g1.append(0)
                i+=1
        i = 0
        j = 0
        list_g2 = []
        g2_name =Genre.objects.get(id=g2).name
        while i < len(list_years):
            if j < len(g2_result) and g2_result[j]['year'] is not None :
                if g2_result[j]['year'] == list_years[i]:
                    list_g2.append(g2_result[j]['dcount'])
                    j += 1
                    i += 1
                else:
                    while g2_result[j]['year'] > list_years[i]:
                        i += 1
                        list_g2.append(0)
            else:
                list_g2.append(0)
                i += 1
        list_result = list()
        for i in range(0,len(list_years)):
            list_result.append({
                'year': list_years[i],
                g1_name: list_g1[i],
                g2_name: list_g2[i]
            })

        return JsonResponse(list_result, safe=False)