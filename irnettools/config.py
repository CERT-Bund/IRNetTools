"""
IRNetTools configuration
"""

# Location of databases
DATABASES = "./databases"

###############################
### Nothing to change below ###
###############################

import os
import sys

try:
    if not os.path.isdir(DATABASES):
        print('DATABASE is not a directory in config.py', file=sys.stderr)
        exit(1)
except TypeError:
    print('Invalid value for DATABASE in config.py', file=sys.stderr)
    exit(1)

# Location of MaxMind GeoLite2 database files
mm_path = os.path.abspath(os.path.join(DATABASES, 'geoip'))
maxmind_country_database = os.path.join(mm_path, 'GeoLite2-Country.mmdb')
maxmind_asn_database = os.path.join(mm_path, 'GeoLite2-ASN.mmdb')

