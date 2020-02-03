"""
IRNetTools configuration
"""

# Maxmind license key
# Since 2019-12-30, a license key is required for downloading Maxmind's GeoLite2 databases
# See <https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/>
MAXMIND_LICENSE_KEY = "xxxxxxxx"

# Location of databases (e.g. Maxmind)
# If not set, defaults to USER_BASE/share/irnettools/databases/
#DATABASES = "~/irnettools-databases"

# Data source for ASN, organization and country information
# Valid values: "cymru" or "maxmind"
ASN_SRC = "maxmind"
ORG_SRC = "maxmind"
COUNTRY_SRC = "maxmind"

#
