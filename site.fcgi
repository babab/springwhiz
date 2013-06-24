#!/usr/bin/python
import sys, os
from django.core.servers.fastcgi import runfastcgi

os.environ['DJANGO_SETTINGS_MODULE'] = 'springwhiz.settings'
runfastcgi(method='threaded', daemonize='false',
           pidfile='/tmp/django-springwhiz.pid')
