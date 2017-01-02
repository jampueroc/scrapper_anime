from __future__ import absolute_import
import datetime
import re
import mechanize
from BeautifulSoup import BeautifulSoup

from celery import current_app as app
from visualizacion.models.anime import Anime
from visualizacion.models.genre import Genre
from visualizacion.models.licensor import Licensor
from visualizacion.models.producer import Producer
from visualizacion.models.status import Status
from visualizacion.models.studio import Studio
from visualizacion.models.title import Title
from visualizacion.models.type import Type


class Scrapper:
    url = 'https://myanimelist.net/'
    suffix = 'anime'

    def __init__(self):
        pass

    @classmethod
    def retrieve_page(cls, url, retries=5):

        try:
            br = mechanize.Browser()
            br.set_handle_robots(False)
            return br.open(url).get_data()
        except Exception:
            if retries:
                return Scrapper.retrieve_page(url, retries-1)
            else:
                raise

    @classmethod
    def animes_urls(cls, pattern, sync=True):
        if not sync:
            print "Using Celery"
        import string
        alphabet = list(string.ascii_lowercase)
        pattern = re.compile("^["+pattern+"]")
        urls_with_error = []

        for letter in alphabet:
            if re.match(pattern,letter):
                print "Scraping letter "+ letter
                number_elements= 0
                while True:
                    url_webpage = '{0}{1}.php?letter={2}&show={3}'.format(
                        cls.url, cls.suffix, letter, number_elements
                    )
                    number_elements += 50
                    try:
                        data = cls.retrieve_page(url_webpage)
                    except Exception:
                        break
                    soup = BeautifulSoup(data)
                    lista = soup.find('div', 'js-categories-seasonal')
                    try:
                        anime_trs = lista.findAll('tr')
                        for anime_tr in anime_trs:
                            try:
                                anime_url=  anime_tr.find('div', 'picSurround').find('a')['href']
                                anime_url = anime_url.encode('ascii', 'ignore')
                                # try:
                                if sync:
                                    create_anime(anime_url)
                                else:
                                    create_anime.apply_async((anime_url,))
                                # except Exception:
                                #     urls_with_error.append(anime_url)
                            except AttributeError:
                                continue
                    except Exception:
                        pass

        print "Finished"
        return urls_with_error


@app.task()
def create_anime(anime_url):
    data = Scrapper.retrieve_page(anime_url)
    soup = BeautifulSoup(data)
    data_anime = soup.find('div', 'js-scrollfix-bottom')
    try:
        anime = Anime.objects.get(url=anime_url)
        print "Updating Anime for url: " + anime_url
        set_atributes(anime, data_anime, True)
    except Anime.DoesNotExist:
        anime = Anime()
        anime.url = anime_url
        print "Creating new Anime for url: " + anime_url
        set_atributes(anime,data_anime,edit_basic_info=True)
    try:
        anime.save()
    except Exception as e:
        create_anime.retry(countdown=2, exc=e, max_retries=5)


def set_atributes(anime, data_anime, edit_basic_info=False):
    atributes = data_anime.findAll('span', "dark_text")
    anime.save()
    blacklist = ['N/A', 'None found','Unknown', 'Not available',
                 'No genres have been added yet.', 'None']
    for atribute in atributes:
        atribute_text = atribute.text
        atribute_value = atribute.parent.text.split(':')[1]
        skip = False

        for element_to_avoid in blacklist:
            if element_to_avoid in atribute_value:
                skip = True
                break
        if skip:
            continue
        if atribute_text.startswith('English:') and edit_basic_info:
            title = Title()
            title.name = atribute_value
            title.save()
            anime.name_english = title
        elif atribute_text.startswith('Synonyms:') and edit_basic_info:
            producers = atribute_value.split(',')
            list_titles = list()
            for name in producers:
                title = Title()
                title.name = atribute_value
                title.save()
                list_titles.append(title)
            anime.name_alternatives.add(*list_titles)
        elif atribute_text.startswith('Japanese:') and edit_basic_info:
            anime.name_japanese = atribute_value

        elif atribute_text.startswith('Type:') and edit_basic_info:
            type , created = Type.objects.get_or_create(name=atribute_value)
            if created:
                type.save()
            anime.type = type
        elif atribute_text.startswith('Episodes:'):
            anime.number_episodes = int(atribute_value)
        elif atribute_text.startswith('Aired:'):
            if 'to' in atribute_value:
                atribute_value = atribute_value.split('to')[0]
            try:
                date = datetime.datetime.strptime(atribute_value.strip(),'%b %d, %Y')
            except ValueError:
                if len(atribute_value.strip()) > 4 :
                    date = datetime.datetime.strptime(atribute_value.strip(), '%b, %Y')
                else:
                    date = datetime.datetime.strptime(atribute_value.strip(), '%Y')
            anime.aired = date

        elif atribute_text.startswith('Status:'):
            anime.status = atribute_value

        # Many to many
        elif atribute_text.startswith('Producers:'):
            producers = atribute_value.split(',')
            list_p = list()
            for p in producers:
                producer, created = Producer.objects.get_or_create(name=p)
                if created:
                    producer.save()
                list_p.append(producer)

            anime.producers.add(*list_p)
        # Many to many
        elif atribute_text.startswith('Licensors:'):
            licensors = atribute_value.split(',')
            list_l = list()
            for l in licensors:
                object, created = Licensor.objects.get_or_create(name=l)
                if created:
                    object.save()
                list_l.append(object)

            anime.licensor.add(*list_l)
        # Many to many
        elif atribute_text.startswith('Studios:'):
            studio = atribute_value.split(',')
            list_s = list()
            for s in studio:
                object, created = Studio.objects.get_or_create(name=s)
                if created:
                    object.save()
                list_s.append(object)

            anime.studios.add(*list_s)

        # Many to many
        elif atribute_text.startswith('Genres:') and edit_basic_info:
            genres = atribute_value.split(',')
            list_g = list()
            for g in genres:
                genre, created = Genre.objects.get_or_create(name=g)
                if created:
                    genre.save()
                list_g.append(genre)
            anime.genres.add(*list_g)
        elif atribute_text.startswith('Rating:'):
            anime.rating = atribute_value
        elif atribute_text.startswith('Score:'):
            anime.score = float(atribute.parent.contents[3].text)
        elif atribute_text.startswith('Ranked:'):
            anime.ranked = int(clean(atribute.parent.contents[2]))
        elif atribute_text.startswith('Popularity:'):
            anime.popularity = int(clean(atribute.parent.contents[2]))
    anime.save()


def clean(string):
    blacklist = ['#',':', '.', ',', '&nbsp;', '\r', '\n', '\t']

    for item in blacklist:
        string = string.replace(item, '')

    return string