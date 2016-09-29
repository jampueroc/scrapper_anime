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
        r'^json/great_producers/$', views.great_producers,
        name='json_great_producers'
    ),
    url(
        r'^json/anual_genres_battle/$', views.anual_genres_battle,
        name='json_anual_genres_battle'
    ),
    url(r'^$', views.IndexView.as_view(),
        name='index'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', staticserve,
            {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
        )