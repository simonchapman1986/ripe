from django.conf import settings
import pygeoip
import os
import gzip
import urllib
import hashlib
import logging


logger = logging.getLogger(__name__)


class GeoIpLookup(object):
    """
    GeoIpLookup

    Utilising the GEOIP module from Maxmind, we can take an IP address, then find out where the call came from.

    The maxmind.dat file must exist for this to work, and relevant settings stored to update the license.

    we use the 'get_country_code' method to get the desired effect.
    """

    def __init__(self):
        self.db_path = settings.PROJECT_ROOT + '/data/geoip/maxmind.dat'
        self.license_key = settings.GEOIP_MAXMIND_LICENSE_KEY
        if not os.path.exists(self.db_path):
            self.update_db()

    def get_country_code(self, ip):
        geo_ip = pygeoip.GeoIP(self.db_path, pygeoip.MEMORY_CACHE)

        try:
            code = geo_ip.country_code_by_addr(ip)
        except Exception:
            logger.exception(u'Country lookup by IP address "{}" failed'.format(ip))
            return None

        if len(code) is 0:
            logger.error(u'Country lookup by IP address "{}" failed'.format(ip))
            return None

        return code

    def update_db(self):
        new_db = self.db_path + '.gz'
        uri = 'http://www.maxmind.com/app/update?license_key={}&md5={}'.format(self.license_key,
                                                                               self.md5sum(self.db_path))
        urllib.urlretrieve(uri, new_db)
        if os.path.getsize(new_db) < 1024:
            with file(new_db) as f:
                s = f.read()
            logger.warning("Can not update GeoIP database: {}".format(s))
            os.remove(new_db)
            raise Exception(s)
        archive = gzip.open(new_db, 'rb')
        with open(self.db_path, 'wb') as destination:
            destination.write(archive.read())
        archive.close()
        os.remove(new_db)

    def md5sum(self, path):
        if not os.path.exists(self.db_path):
            return 0
        with open(path, 'rb') as f:
            md5 = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                md5.update(data)
            return md5.hexdigest()

GEO_IP_LOOKUP = GeoIpLookup()
