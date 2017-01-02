"""visualizacion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import os

from django.views.decorators.cache import cache_page
from django.views.static import serve as staticserve
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(
        r'^json/genre/$', views.genre_percent,
        name='json_genre_percent'
    ),
    url(
        r'^json/null/$', views.get_number_nulls,
        name='json_null'
    ),
    url(
        r'^json/producer/$', views.get_genres_by_producers,
        name='json_producer'
    ),
    url(
        r'^json/anual_genres_ranking/$', views.anual_genres_ranking,
        name='json_anual_genres_ranking'
    ),
    url(
        r'^json/genre_ranking/(?P<pk>\d+)/$', views.GenreDataView.as_view(),
        name='json_genre_ranking'
    ),
    url(
        r'^json/genre_graph/(?P<pk>\d+)/$', views.GenreDataGraphView.as_view(),
        name='json_genre_graph'
    ),
    url(
        r'^json/versus_graph/$', views.VersusGraphView.as_view(),
        name='json_versus_graph'
    ),
    url(
        r'^json/producer_graph/(?P<pk>\d+)/$', views.ProducerDataGraphView.as_view(),
        name='json_producer_graph'
    ),
    url(
        r'^json/producer_ranking/(?P<pk>\d+)/$', views.ProducerDataView.as_view(),
        name='json_producer_ranking'
    ),
    url(
        r'^json/great_producers/$', views.great_producers,
        name='json_great_producers'
    ),
    url(
        r'^json/anual_genres_battle/$', views.anual_genres_battle,
        name='json_anual_genres_battle'
    ),
    url(r'^d3/$', views.TryingD3.as_view(),
        name='try_d3'),
    url(r'^genre/(?P<pk>\d+)/$', views.GenreDetail.as_view(),
        name='genre'),
    url(r'^final/$', cache_page(60 * 60 * 12 * 365, key_prefix="final")(views.FinalVersionView.as_view()),
        name='final'),
    url(r'^$', views.IndexView.as_view(),
        name='index'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', staticserve,
            {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
        )