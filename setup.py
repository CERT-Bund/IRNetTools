import os
import setuptools
import irnettools

cur_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(cur_dir, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(cur_dir, 'requirements.txt')) as f:
    requires = f.read().splitlines()

setuptools.setup(
    name = 'irnettools',
    version = irnettools.version,
    author = 'Thomas Hungenberg',
    author_email = "th@cert-bund.de",
    description = 'A set of tools useful for processing\
    network data like IP addresses, URLs or email credentials\
    while handling security incidents.',
    long_description = long_description,
    url = "https://github.com/cert-bund/irnettools",
    packages = ['irnettools'],
    install_requires = requires,
    python_requires = '>=3.5',
    scripts = ['bin/add_abuse_contact',
               'bin/add_asgeo',
               'bin/add_email_mx',
               'bin/hostinfo',
               'bin/process_urls',
               'bin/process_email_credentials',
               'bin/update-irnettools-databases',
    ],
    keywords = 'incident response network tools cert',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Topic :: Security'
    ],
)
