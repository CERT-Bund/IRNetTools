"""
Abuse contact lookup using DNS based service provided
by Abusix.

Copyright (c) 2018 Thomas Hungenberg

Licensed under GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>

Requires dnspython (Package python3-dnspython on Debian).
"""

import irnettools.errors
import irnettools.validate

try:
    import dns.resolver
    import dns.reversename
except ImportError:
    dns = None

class Lookup:
    """Abuse contact lookup using Abusix service."""
    def __init__(self, config):
        if dns is None:
            raise ImportError('Could not import dnspython')

        self.config = config
        self.resolver = dns.resolver.Resolver()
        self.abusecache = {}

    def abuse_contact(self, ip):
        """
        Returns abuse contact provided by Abusix for IP address.
        """
        if ip in self.abusecache:
            # result in cache
            return self.abusecache[ip]
        else:
            # result not in cache
            if irnettools.validate.ipv4(ip):
                queryname = str(dns.reversename.from_address(ip)).replace('in-addr.arpa.', 'abuse-contacts.abusix.org')
            elif irnettools.validate.ipv6(ip):
                queryname = str(dns.reversename.from_address(ip)).replace('ip6.arpa.', 'abuse-contacts.abusix.org')
            else:
                raise irnettools.errors.InvalidIPError

            # get abuse contact information
            try:
                answers = self.resolver.query(queryname, 'TXT')
                # if there are multiple TXT records, we just take the first one
                self.abusecache[ip] = answers[0].strings[0].decode('ascii')
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                # No TXT record
                self.abusecache[ip] = None
            except dns.resolver.NoNameservers as e:
                # No nameserver
                raise irnettools.errors.DNSError('No nameservers available')

            return self.abusecache[ip]
