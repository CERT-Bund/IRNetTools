"""
Lookup progress information

Copyright (c) 2019 Thomas Hungenberg

Licensed under GNU Affero General Public License v3.0
<http://www.gnu.org/licenses/agpl-3.0.html>
"""

import io
import sys
import irnettools.errors

class Progress:
    """Lookup progress information"""
    def __init__(self, filename):
        self.totallines = 0
        self.currentline = 0

        if filename == '-':
            print ("Warning: Progress not available when reading from stdin", file=sys.stderr)
        else:
            try:
                with io.open(filename, 'r') as file:
                    print ("Counting lines in input file.", file=sys.stderr)
                    lines = 0
                    for line in file:
                        lines += 1
                    self.totallines = lines
                    if lines > 0:
                        print ("Total number of lines: %s" % lines, file=sys.stderr)
                    else:
                        print ("Empty input file.", file=sys.stderr)
            except IOError as e:
                 raise irnettools.errors.ProgressError(str(e))

    def next(self):
        if self.totallines > 0:
            self.currentline += 1
            print ("Processing line %s of %s" % (self.currentline, self.totallines), file=sys.stderr, end='\r', flush=True)
