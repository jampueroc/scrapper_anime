from django.contrib import admin

from visualizacion.models.anime import Anime
from visualizacion.models.genre import Genre
from visualizacion.models.licensor import Licensor
from visualizacion.models.producer import Producer
from visualizacion.models.status import Status
from visualizacion.models.studio import Studio
from visualizacion.models.title import Title
from visualizacion.models.type import Type

admin.site.register(Anime)
admin.site.register(Genre)
admin.site.register(Licensor)
admin.site.register(Producer)
admin.site.register(Status)
admin.site.register(Studio)
admin.site.register(Type)
admin.site.register(Title)
