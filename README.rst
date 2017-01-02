=============================
Scrapper Anime from AnimeList
=============================
This is a basic scrapper to get Anime information

Installation
============

For use memcached, you need to install in ubuntu:
sudo apt-get install -y libmemcached-dev zlib1g-dev libssl-dev python-dev build-essential


This is a Django project, in order to run it just download or clone the project and install its dependencies using pip::

    pip install -r requirements.txt

The use of virtualenv is recommended to prevent package clashes, otherwise you may need superuser prvileges to execute the command above.


Using Redis
===========
You need to install redis to use with celery ::
http://redis.io/download


Using Celery:

For install celery ::
http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html

Creating Virtual Env
====================

In the requirements of the project we recommend use virtualwrapper because is easy to use. You can see how to use in ::
https://virtualenvwrapper.readthedocs.io/en/latest/


For use the scrapper
====================

To run redis (if you install redis-server, local ubication) ::
./redis-server

To run celery (In the main folder of the project) ::
celery -A visualizacion worker --loglevel=info

Or to run in demon mode, saving the log:
celery multi start 1 -A visualizacion -l info -c8 --logfile=celery/logs/celery.log

To stop in the first case, is enough press ctrl-c and in the second you have to use::
celery multi stop 1 -A visualizacion -l info -c8 --logfile=celery/logs/celery.log

For see the logs in the first case show in console and in the second you can use::
tail celery/logs/celery.log -l



Activate virtual Env (eg. vis):
workon vis

Run command for scrapper urls:
python manage.py update_anime_list


This command has an optional argument --alphabet [a-z] this allow search in a specific letter or in a range a-c.

For run website
===============

Activate virtual Env (eg. vis):
workon vis

Load data scrapper (if you don't want to scan):
python manage.py loaddata data_(date).json


Run django project:
python manage.py runserver

