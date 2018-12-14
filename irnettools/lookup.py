"""
Main Lookup class providing config

Copyright (c) 2018 Thomas Hungenberg

Licensed under GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>
"""

import os
import sys
import irnettools.errors
import irnettools.config
import irnettools.dns
import irnettools.abusix
import irnettools.cymru
import irnettools.maxmind

class Lookup:
    """Main Lookup class providing config"""
    def __init__(self):
        try:
            db = irnettools.config.DATABASES
        except AttributeError:
            raise irnettools.errors.ConfigError('DATABASES not defined in config.py')

        try:
            if not os.path.isdir(db):
                raise irnettools.errors.ConfigError('DATABASES directory does not exist. Check config.py.')
        except TypeError:
            raise irnettools.errors.ConfigError('Invalid value for DATABASES in config.py')

        try:
            asn_src = irnettools.config.ASN_SRC
        except AttributeError:
            raise irnettools.errors.ConfigError('ASN_SRC not defined in config.py')
        if asn_src not in ['cymru', 'maxmind']:
            raise irnettools.errors.ConfigError('Invalid value for ASN_SRC in config.py')

        try:
            org_src = irnettools.config.ORG_SRC
        except AttributeError:
            raise irnettools.errors.ConfigError('ORG_SRC not defined in config.py')
        if org_src not in ['cymru', 'maxmind']:
            raise irnettools.errors.ConfigError('Invalid value for ORG_SRC in config.py')

        try:
            country_src = irnettools.config.COUNTRY_SRC
        except AttributeError:
            raise irnettools.errors.ConfigError('COUNTRY_SRC not defined in config.py')
        if country_src not in ['cymru', 'maxmind']:
            raise irnettools.errors.ConfigError('Invalid value for COUNTRY_SRC in config.py')

        self.config = {}
        self.config['asn_src'] = asn_src
        self.config['org_src'] = org_src
        self.config['country_src'] = country_src

        if asn_src == 'maxmind' or org_src == 'maxmind' or country_src == 'maxmind':
            # Maxmind databases required
            self.config['use_maxmind'] = True
            # Path to databases
            self.config['db_path'] = os.path.abspath(os.path.join(irnettools.config.DATABASES, ''))
            # Location of MaxMind GeoLite2 database files
            mm_path = os.path.abspath(os.path.join(self.config['db_path'], 'maxmind'))
            self.config['maxmind_country_database'] = os.path.join(mm_path, 'GeoLite2-Country.mmdb')
            self.config['maxmind_asn_database'] = os.path.join(mm_path, 'GeoLite2-ASN.mmdb')
        else:
            # Maxmind databases not needed
            self.config['use_maxmind'] = False

        self.dnslookup = irnettools.dns.Lookup(self.config)
        self.abusixlookup = irnettools.abusix.Lookup(self.config)
        self.cymrulookup = irnettools.cymru.Lookup(self.config)
        if self.config['use_maxmind']:
            self.maxmindlookup = irnettools.maxmind.Lookup(self.config)

    def ip(self, hostname):
        """
        Resolves hostname to IP address.
        Tries IPv4 first, then IPv6.
        If hostname resolves to multiple IPs, only returns the first IP.
        If hostname does not resolve, returns None.
        """
        return self.dnslookup.ip(hostname)

    def ipv4(self, hostname):
        """
        Resolves hostname to IPv4 address.
        If hostname resolves to multiple IPs, only returns the first IP.
        If hostname does not resolve, returns None.
        """
        return self.dnslookup.ipv4(hostname)

    def ipv6(self, hostname):
        """
        Resolves hostname to IPv6 address.
        If hostname resolves to multiple IPs, only returns the first IP.
        If hostname does not resolve, returns None.
        """
        return self.dnslookup.ipv6(hostname)

    def hostname(self, ip):
        """
        Returns reverse lookup (PTR) for IP address.
        If there is no PTR record, returns None.
        """
        return self.dnslookup.hostname(ip)

    def mx(self, hostname):
        """
        Returns MX with lowest preference (highest priority) for hostname.
        Returns None if no MX configured.
        """
        return self.dnslookup.mx(hostname)

    def abuse_contact(self, ip):
        """
        Returns abuse contact for IP address.
        """
        return self.abusixlookup.abuse_contact(ip)

    def asn(self, ip):
        """
        Returns AS number announcing IP address
        or None if IP address not in database
        """
        if self.config['asn_src'] == "maxmind":
            return self.maxmindlookup.asn(ip)
        elif self.config['asn_src'] == "cymru":
            return self.cymrulookup.asn(ip)

    def organization(self, ip):
        """
        Returns organization for IP address
        or None if IP address not in database
        """
        if self.config['org_src'] == "maxmind":
            return self.maxmindlookup.organization(ip)
        elif self.config['org_src'] == "cymru":
            return self.cymrulookup.organization(ip)

    def country(self, ip):
        """
        Returns country code for IP address
        or None if IP address not in database
        """
        if self.config['country_src'] == "maxmind":
            return self.maxmindlookup.country(ip)
        elif self.config['country_src'] == "cymru":
            return self.cymrulookup.country(ip)
