"""
This module provides a class for performing various
DNS lookups with caching of results for speedup.

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
    """Provides methods for IP lookups with caching of results for speedup."""
    def __init__(self, config):
        if dns is None:
            raise ImportError('Could not import dnspython')

        self.config = config
        self.resolver = dns.resolver.Resolver()
        self.hosttoipv4cache = {}
        self.hosttoipv6cache = {}
        self.iptohostcache = {}
        self.hosttomxcache = {}

    def ipv4(self, hostname):
        """
        Resolves hostname to IPv4 address.
        If hostname resolves to multiple IPs, only returns the first IP.
        If hostname does not resolve, returns None.
        """
        if not irnettools.validate.hostname(hostname):
            raise irnettools.errors.InvalidHostnameError

        if hostname in self.hosttoipv4cache:
            # result in cache
            return self.hosttoipv4cache[hostname]
        else:
            # result not in cache
            try:
                answers = self.resolver.query(hostname, 'A')
                # if the hostname resolves to multiple IPs, we only take the first one
                ip = str(answers[0].address)
                self.hosttoipv4cache[hostname] = ip
                return ip
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                # hostname does not resolve
                self.hosttoipv4cache[hostname] = None
                return None
            except dns.resolver.NoNameservers as e:
                # No nameserver
                raise irnettools.errors.DNSError('No nameservers available')

    def ipv6(self, hostname):
        """
        Resolves hostname to IPv6 address.
        If hostname resolves to multiple IPs, only returns the first IP.
        If hostname does not resolve, returns None.
        """
        if not irnettools.validate.hostname(hostname):
            raise irnettools.errors.InvalidHostnameError

        if hostname in self.hosttoipv6cache:
            # result in cache
            return self.hosttoipv6cache[hostname]
        else:
            # result not in cache
            try:
                answers = self.resolver.query(hostname, 'AAAA')
                # if the hostname resolves to multiple IPs, we only take the first one
                ip = str(answers[0].address)
                self.hosttoipv6cache[hostname] = ip
                return ip
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                # hostname does not resolve
                self.hosttoipv6cache[hostname] = None
                return None
            except dns.resolver.NoNameservers as e:
                # No nameserver
                raise irnettools.errors.DNSError('No nameservers available')

    def ip(self, hostname):
        """
        Resolves hostname to IP address.
        Tries IPv4 first, then IPv6.
        If hostname resolves to multiple IPs, only returns the first IP.
        If hostname does not resolve, returns None.
        """
        ip = self.ipv4(hostname)
        if not ip:
            ip = self.ipv6(hostname)
        return ip

    def hostname(self, ip):
        """
        Returns reverse lookup (PTR) for IP address.
        If there is no PTR record, returns None.
        """
        if not irnettools.validate.ip(ip):
            raise irnettools.errors.InvalidIPError

        if ip in self.iptohostcache:
            # result in cache
            return self.iptohostcache[ip]
        else:
            # result not in cache
            try:
                query = dns.reversename.from_address(ip)
                answers = self.resolver.query(query, 'PTR')
                hostname = str(answers[0].target).rstrip('\.')
                self.iptohostcache[ip] = hostname
                return hostname
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                # hostname does not resolve
                self.iptohostcache[ip] = None
                return None
            except dns.resolver.NoNameservers as e:
                # No nameserver
                raise irnettools.errors.DNSError('No nameservers available')

    def mx(self, hostname):
        """
        Returns MX with lowest preference (highest priority) for hostname.
        Returns None if no MX configured.
        """
        if not irnettools.validate.hostname(hostname):
            raise irnettools.errors.InvalidHostnameError

        if hostname in self.hosttomxcache:
            # result in cache
            return self.hosttomxcache[hostname]
        else:
            # result not in cache
            try:
                answers = self.resolver.query(hostname, 'MX')
                mxhostname = None
                pref = None
                for rdata in answers:
                    if not pref or rdata.preference < pref:
                        mxhostname = str(rdata.exchange).rstrip('\.')
                        pref = rdata.preference
                self.hosttomxcache[hostname] = mxhostname
                return mxhostname
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                # No MX configured
                self.hosttomxcache[hostname] = None
                return None
            except dns.resolver.NoNameservers as e:
                # No nameserver
                raise irnettools.errors.DNSError('No nameservers available')

#
