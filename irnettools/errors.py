"""
Custom errors for IRNetTools

Copyright (c) 2018-2019 Thomas Hungenberg

Licensed under GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>
"""

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ConfigError(Error):
    """Exception raised for config errors."""
    pass

class DNSError(Error):
    """Exception raised for DNS errors."""
    pass

class DNSFatalError(Error):
    """Exception raised for fatal DNS errors (e.g. no nameservers available)."""
    pass

class InvalidHostnameError(Error):
    """Exception raised for invalid hostnames."""
    pass

class InvalidIPError(Error):
    """Exception raised for invalid hostnames."""
    pass

class IP2ASNLookupError(Error):
    """Exception raised for invalid AS lookup responses."""
    pass

class MaxmindError(Error):
    """Exception raised for GeoIP related errors."""
    pass
