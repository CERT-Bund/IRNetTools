"""
Maxmind GeoLite2 Country/ASN database lookups

Copyright (c) 2018 Thomas Hungenberg

Licensed under GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>

Requires geoip2
"""

import irnettools.errors
import irnettools.validate

try:
    import geoip2.database
    import geoip2.errors
except ImportError:
    geoip2 = None

class Lookup:
    """
    Maxmind database lookup
    """
    def __init__(self, config):
        self.config = config
        if geoip2 is None:
            raise ImportError('Could not import geoip2')

        try:
            self.countrydb = geoip2.database.Reader(self.config['maxmind_country_database'])
        except FileNotFoundError:
            raise irnettools.errors.MaxmindError('Maxmind GeoLite2 Country database file not found. Check configuration or run \'update-irnettools-databases\'.')

        try:
            self.asndb = geoip2.database.Reader(self.config['maxmind_asn_database'])
        except FileNotFoundError:
            raise irnettools.errors.MaxmindError('Maxmind GeoLite2 ASN database file not found. Check configuration or run \'update-irnettools-databases\'.')

        self.iptocountrycache= {}
        self.iptoasncache= {}
        self.iptoorgcache= {}

    def asn(self, ip):
        """
        Returns AS number announcing IP address
        or None if IP address not in database
        """
        if not irnettools.validate.ip(ip):
            raise irnettools.errors.InvalidIPError

        if ip in self.iptoasncache:
            # result in cache
            return self.iptoasncache[ip]
        else:
            try:
                asn = self.asndb.asn(ip).autonomous_system_number
                self.iptoasncache[ip] = asn
                return asn
            except geoip2.errors.AddressNotFoundError:
                self.iptoasncache[ip] = None
                return None

    def organization(self, ip):
        """
        Returns organization for IP address
        or None if IP address not in database
        """
        if not irnettools.validate.ip(ip):
            raise irnettools.errors.InvalidIPError

        if ip in self.iptoorgcache:
            # result in cache
            return self.iptoorgcache[ip]
        else:
            try:
                org = self.asndb.asn(ip).autonomous_system_organization
                self.iptoorgcache[ip] = org
                return org
            except geoip2.errors.AddressNotFoundError:
                self.iptoorgcache[ip] = None
                return None

    def country(self, ip):
        """
        Returns country code for IP address
        or None if IP address not in database
        """
        if not irnettools.validate.ip(ip):
            raise irnettools.errors.InvalidIPError

        if ip in self.iptocountrycache:
            # result in cache
            return self.iptocountrycache[ip]
        else:
            try:
                country = self.countrydb.country(ip).registered_country.iso_code
                self.iptocountrycache[ip] = country
                return country
            except geoip2.errors.AddressNotFoundError:
                self.iptocountrycache[ip] = None
                return None
