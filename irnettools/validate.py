"""
This module provides functions for validating ip addresses,
email adrresses, etc.

Copyright (c) 2018 Thomas Hungenberg

Licensed under GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>
"""

import re
import ipaddress

def ip(ip):
    """Returns True if ip is a valid IP address, None otherwise."""
    if ipv4(ip) or ipv6(ip):
        return True
    else:
        return False

def ipv4(ip):
    """Returns True if ip is a valid IPv4 address, None otherwise."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def ipv6(ip):
    """Returns True if ip is a valid IPv6 address, None otherwise."""
    try:
        ipaddress.IPv6Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def hostname(hostname):
    """Returns True if hostname is a valid hostname, None otherwise."""
    if re.match('(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}|[a-zA-Z0-9]+)$', hostname):
        return True
    else:
        return False
    
def fqdn(hostname):
    """Returns True if hostname is a fully-qualified domain name, None otherwise."""
    if re.match('(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63})$', hostname):
        return True
    else:
        return False
    
def email(email):
    """Returns True if email is a valid email address, None otherwise."""
    if re.match("^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email):
        return True
    else:
        return False

#
