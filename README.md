# Incident Response Network Tools

A set of tools useful for processing network data like IP addresses,
URLs or email credentials when handling security incidents.

Requires Python 3.5 or later.

Uses Maxmind GeoLite2 databases (https://dev.maxmind.com/geoip/geoip2/geolite2/).

Uses IP2ASN lookup service provided by Team Cymru (https://www.team-cymru.com/IP-ASN-mapping.html).

Uses abuse contact lookup service provided by Abusix (https://www.abusix.com/contactdb).

**Important note:**  
Since 2019-12-30, a license key is required for downloading Maxmind's GeoLite2 databases  
(see https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/).

## Tools

### add_abuse_contact

Takes a CSV file with column 'ip' and arbitrary additional columns
as input and returns each row with abuse contact information
provided by Abusix added for the respective IP address.

    $ cat sample-malware.csv
    "timestamp","ip","malware"
    "2018-11-20 16:05:30","115.164.72.50","Malware_ABC"
    "2018-11-20 20:02:30","14.189.152.180","Malware_123"
    "2018-11-20 23:57:56","79.208.10.20","Malware_XYZ"

    $ add_abuse_contact sample-malware.csv
    "timestamp","ip","malware","abuse_contact"
    "2018-11-20 16:05:30","115.164.72.50","Malware_ABC","abuse@digi.com.my"
    "2018-11-20 20:02:30","14.189.152.180","Malware_123","hm-changed@vnnic.vn"
    "2018-11-20 21:57:56","79.208.10.20","Malware_XYZ","abuse@telekom.de"

### add_asgeo

Takes a CSV file with column 'ip' and arbitrary additional columns
as input and returns each row with ASN, organization and country
information for the respective IP address added.

    $ cat sample-malware.csv
    "timestamp","ip","malware"
    "2018-11-20 16:05:30","115.164.72.50","Malware_ABC"
    "2018-11-20 20:02:30","14.189.152.180","Malware_123"
    "2018-11-20 23:57:56","79.208.10.20","Malware_XYZ"

    $ add_asgeo sample-malware.csv
    "timestamp","ip","malware","asn","org","country"
    "2018-11-20 16:05:30","115.164.72.50","Malware_ABC","4818","DiGi Telecommunications Sdn. Bhd.","MY"
    "2018-11-20 20:02:30","14.189.152.180","Malware_123","45899","VNPT Corp","VN"
    "2018-11-20 21:57:56","79.208.10.20","Malware_XYZ","3320","Deutsche Telekom AG","DE"
    "2018-11-20 23:24:56","2001:470:1:18::125","Malware_456","6939","Hurricane Electric LLC","US"

### add_host_ip

Takes a CSV file with column 'hostname' and arbitrary additional columns
as input and returns each row with the respective IP address added.
Tries to resolve hostname to IPv4 first, then tries IPv6.

    $ cat sample-hostport.csv
    "hostname","port"
    "www.google.com","443"
    "smtp.gmx.de","25"
    "ipv6.test-ipv6.com","80"

    $ add_host_ip sample-hostport.csv
    "ip","hostname","port"
    "216.58.205.228","www.google.com","443"
    "212.227.17.168","smtp.gmx.de","25"
    "2001:470:1:18::119","ipv6.test-ipv6.com","80",""

### add_email_mx

Takes a CSV file with column 'email' and arbitrary additional columns
as input and returns each row with the IP address and hostname of the
corresponding MX with lowest preference (highest priority) added.

    $ cat sample-email.csv
    "email","count"
    "lieschen.mueller@gmx.de","5"
    "max.mustermann@gmail.com","10"
    "alice.wonderland@yahoo.com","15"

    $ add_email_mx sample-email.csv
    "ip","mx","email","count"
    "212.227.15.9","mx00.emig.gmx.net","lieschen.mueller@gmx.de","5"
    "108.177.15.26","gmail-smtp-in.l.google.com","max.mustermann@gmail.com","10"
    "98.136.102.54","mta7.am0.yahoodns.net","alice.wonderland@yahoo.com","15"

### hostinfo

Takes a single hostname/IP address or a file containing a list of
hostnames/IP addresses (one record per line) as input and returns
the IP address and corresponding hostname along with AS number,
organization and country information in CSV format.

    $ hostinfo smtp.gmx.de
    "ip","hostname","asn","org","country"
    "212.227.17.168","smtp.gmx.de","8560","1&1 Internet SE","DE"

    $ hostinfo 216.58.213.195
    "ip","hostname","asn","org","country"
    "216.58.213.195","ham02s15-in-f195.1e100.net","15169","Google LLC","US"

    $ hostinfo -f sample-hosts.txt
    "ip","hostname","asn","org","country"
    "216.58.212.164","www.google.com","15169","Google LLC","US"
    "212.227.17.168","smtp.gmx.de","8560","1&1 Internet SE","DE"
    "2001:470:1:18::125","ipv6.test-ipv6.com","6939","Hurricane Electric LLC","US"

### process_urls

Takes a list of URLs as input and returns the (sanitized) URLs along
with the IP address the hostname resolves to in CSV format. Optionally
checks HTTP status code for http(s) URLs.

    $ cat sample-urls.txt
    https://www.google.com/intl/en/about/?fg=1&utm_source=google-US
    HTTP://www.heise.de
    ftp://134.76.12.6/pub/FreeBSD/README.TXT
    
    $ process_urls -n -s sample-urls.txt
    "ip","url","http_status"
    "172.217.16.68","https://www[.]google[.]com/intl/en/about/?fg=1&utm_source=google-US","200"
    "193.99.144.85","http://www[.]heise[.]de","200"
    "134.76.12.6","ftp://134[.]76[.]12[.]6/pub/FreeBSD/README.TXT",""

### process_email_credentials

Takes a list of email credentials as input and returns the IP address
of the corresponding MX with lowest preference (highest priority), the
hostname of the MX, the email address and the (sanitized) password in
CSV format.

    $ cat sample-credentials.txt
    lieschen.mueller@gmx.de:pass1234
    max.mustermann@gmail.com:topsecret55
    alice.wonderland@yahoo.com:alwola123

    $ process_email_credentials -s sample-credentials.txt
    "ip","mx","username","password"
    "212.227.15.9","mx00.emig.gmx.net","lieschen.mueller@gmx.de","pa******"
    "173.194.76.26","gmail-smtp-in.l.google.com","max.mustermann@gmail.com","to******"
    "67.195.229.59","mta5.am0.yahoodns.net","alice.wonderland@yahoo.com","al******"

### csv_recol

Extract (and rearrange) columns from a CSV file.

    $ cat sample-hostinfo.csv
    "ip","hostname","asn","org","country"
    "216.58.212.164","www.google.com","15169","Google LLC","US"
    "212.227.17.168","smtp.gmx.de","8560","1&1 Internet SE","DE"
    "2001:470:1:18::125","ipv6.test-ipv6.com","6939","Hurricane Electric LLC","US"

    $ csv_recol sample-hostinfo.csv country asn ip hostname
    "country","asn","ip","hostname"
    "US","15169","216.58.212.164","www.google.com"
    "DE","8560","212.227.17.168","smtp.gmx.de"
    "US","6939","2001:470:1:18::125","ipv6.test-ipv6.com"

## Concatenation of tools

All tools taking CSV data as input can also read from stdin,
so they can be concatenated like this:

    $ add_host_ip sample-hostport.csv | add_asgeo - | add_abuse_contact -
    "ip","hostname","port","asn","org","country","abuse_contact"
    "172.217.23.132","www.google.com","443","15169","Google LLC","US","network-abuse@google.com"
    "212.227.17.168","smtp.gmx.de","25","8560","1&1 Internet SE","DE","abuse@oneandone.net"
    "2001:470:1:18::119","ipv6.test-ipv6.com","80","6939","Hurricane Electric LLC","US","abuse@he.net"

## Configuration

Configuration is done in `irnettools/config.py`.

| Variable | Value |
| --- | --- |
| `DATABASES` | Path to databases. If not set, defaults to `USER_BASE/share/irnettools/databases/` |
| `ASN_SRC` | Data source for ASN lookups: `cymru` or `maxmind` |
| `ORG_SRC` | Data source for organization lookups: `cymru` or `maxmind` |
| `COUNTRY_SRC` | Data source for country lookups: `cymru` or `maxmind` |

## Databases

IRNetTools uses Maxmind GeoLite2 databases for ASN, organization and country lookups.

Run `update-irnettools-databases` to install/update the databases.

By default, databases are stored in `USER_BASE/share/irnettools/databases/`.
To change the location of the databases, set variable `DATABASES` in `irnettools/config.py`.

## Installation

### Installation in user's home

Install IRNetTools from github

    $ pip3 install --user https://github.com/cert-bund/irnettools/archive/master.zip

Add the following lines to your shell startup file (e.g. `~/.bashrc` or `~/.profile`)

    export PY_USER_BIN=$(/usr/bin/env python3 -c 'import site; print(site.USER_BASE + "/bin")')
    export PATH=$PATH:$PY_USER_BIN

Re-read the shell startup file (e.g. `source ~/.bashrc`).

Set your Maxmind license key in `irnettools/config.py` and run
`update-irnettools-databases` to download and install databases.

### Installation in a Python virtual environment

    $ python3 -m venv irnettools
    $ cd irnettools
    $ source bin/activate
    $ pip3 install https://github.com/cert-bund/irnettools/archive/master.zip

Set your Maxmind license key in `irnettools/config.py` and run
`update-irnettools-databases` to download and install databases.
    
## License
This software is licensed under GNU Affero General Public License version 3.
