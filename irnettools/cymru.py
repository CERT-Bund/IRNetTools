"""
ASN, organization and country information lookups
using Team Cymru IP2ASN service

Copyright (c) 2018 Thomas Hungenberg

Licensed under GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>

Requires dnspython (Package python3-dnspython on Debian).
"""

import re
import irnettools.errors
import irnettools.validate

try:
    import dns.resolver
    import dns.reversename
except ImportError:
    dns = None

class Lookup:
    """Team Cymru IP2ASN lookups"""
    def __init__(self, config):
        
        if dns is None:
            raise ImportError('Could not import dnspython')

        self.config = config
        self.resolver = dns.resolver.Resolver()
        self.iptoasncache= {}
        self.iptocountrycache= {}
        self.iptoorgcache= {}

    def asn(self, ip):
        """
        Returns AS number for IP address
        or None if not available
        """
        if not irnettools.validate.ip(ip):
            raise irnettools.errors.InvalidIPError

        if ip in self.iptoasncache:
            # result in cache
            return self.iptoasncache[ip]
        else:
            self._getasinfo(ip)
            return self.iptoasncache[ip]

    def organization(self, ip):
        """
        Returns organization for IP address
        or None if not available
        """
        if not irnettools.validate.ip(ip):
            raise irnettools.errors.InvalidIPError

        if ip in self.iptoorgcache:
            # result in cache
            return self.iptoorgcache[ip]
        else:
            self._getasinfo(ip)
            return self.iptoorgcache[ip]

    def country(self, ip):
        """
        Returns country information for IP address
        or None if not available
        """
        if not irnettools.validate.ip(ip):
            raise irnettools.errors.InvalidIPError

        if ip in self.iptocountrycache:
            # result in cache
            return self.iptocountrycache[ip]
        else:
            self._getasinfo(ip)
            return self.iptocountrycache[ip]

    def _getasinfo(self, ip):
        """
        Get ASN, organization and country information
        for IP address and store in cache
        """
        if irnettools.validate.ipv4(ip):
            queryname = str(dns.reversename.from_address(ip)).replace('in-addr.arpa.', 'origin.asn.cymru.com')
        elif irnettools.validate.ipv6(ip):
            queryname = str(dns.reversename.from_address(ip)).replace('ip6.arpa.', 'origin6.asn.cymru.com')
        else:
            raise irnettools.errors.InvalidIPError

        try:
            answers = self.resolver.query(queryname, 'TXT')
            # if there are multiple TXT records, we only take the first one
            info = answers[0].strings[0].decode('ascii')
            fields = info.split('|')
            if len(fields) == 5:
                self.iptoasncache[ip] = fields[0].strip()
                self.iptocountrycache[ip] = fields[2].strip()
            else:
                raise irnettools.errors.IP2ASNLookupError
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            # No TXT record
            self.iptoasncache[ip] = None
            self.iptocountrycache[ip] = None
            self.iptoorgcache[ip] = None
            return
        except dns.resolver.NoNameservers as e:
            # No nameserver
            raise irnettools.errors.DNSError('No nameservers available')

        queryname = 'AS' + self.iptoasncache[ip]  + ".asn.cymru.com"
        try:
            answers = self.resolver.query(queryname, 'TXT')
            # if there are multiple TXT records, we only take the first one
            info = answers[0].strings[0].decode('ascii')
            fields = info.split('|')
            if len(fields) == 5:
                self.iptoorgcache[ip] = re.sub(', [A-Z]{2}$', '', fields[4].strip())
            else:
                raise irnettools.errors.InvalidASLookupError
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            # No TXT record
            self.iptoorgcache[ip] = ''
        except dns.resolver.NoNameservers as e:
            # No nameserver
            raise irnettools.errors.DNSError('No nameservers available')
            
#
