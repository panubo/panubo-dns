from django.conf import settings

from squab.connection import CouchConnection


def connection(name):
    return CouchConnection(settings.COUCH_DATABASES[name]['HOST'],
                                     settings.COUCH_DATABASES[name]['NAME'],
                                     settings.COUCH_DATABASES[name]['USER'],
                                     settings.COUCH_DATABASES[name]['PASS'],
                                     settings.COUCH_IGNORE_MISSING)