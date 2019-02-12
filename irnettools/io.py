"""
Input/Output functions

Copyright (c) 2019 Thomas Hungenberg

Licensed under GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>
"""

import sys

def printerror(message, newline=True):
    if newline:
        print('', file=sys.stderr)
    print('Error: %s' % message, file=sys.stderr)

#
