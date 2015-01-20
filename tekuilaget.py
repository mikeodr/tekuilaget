#!/usr/bin/env python
"""
tekuilaget.py

An NZBGet scheduler script. Set a threshold to pause NZBGet during tracked
hours.

Copyright (C) 2014  Mike O'Driscoll <mike@mikeodriscoll.ca>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
############################################################################
### NZBGET SCHEDULER SCRIPT                                              ###
# Script to check your Teksavvy cap and pause downloading during tracked hours.
#
# If threshold is exceeded then pause. Set this script to run at 8am. Set an
# unpause scheduler to run at 2am to work with this script.
#
# Info about scheduler-script:
# Author: Mike O'Driscoll (mike@mikeodriscoll.ca).
# Web-site: http://github.com/mikeodr.
# License GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html).
#
# Requires the following python modules installed:
# pynzbget: http://github.com/caronc/pynzbget.
# tekuila: http://github.com/mikeodr/tekuila
#

############################################################################
### OPTIONS                                                              ###

## General

#
# Enable NZBGet debug logging (yes, no)
# Debug=no

# Set your Teksavvy API Key
#Key=

# Set your Cap in GB
#Cap=

# Set your pause ratio, 0.0 to 1.0
#Ratio=
#

### NZBGET SCHEDULER SCRIPT                                              ###
############################################################################

from nzbget import ScanScript
import tekuila
import xmlrpclib
from sys import exit


# Now define your class while inheriting the rest
class TekuilaGet(ScanScript):
    def main(self, *args, **kwargs):
        # write all of your code here you would have otherwise put in the
        # script

        if not self.validate():
            # No need to document a failure, validate will do that
            # on the reason it failed anyway
            return False

        host = self.get('CONTROLIP')
        port = self.get('CONTROLPORT')
        username = self.get('CONTROLUSERNAME')
        password = self.get('CONTROLPASSWORD')

        if not username and not password:
            url = "http://%s:%s@%s:%s/xmlrpc" % \
                (username, password, host, port)
        else:
            url = "http://%s:%s/xmlrpc" % (host, port)
        server = xmlrpclib.Server(url)

        key = self.get('Key')
        cap = self.get('Cap')
        ratio = self.get('Ratio')
        tekq = tekuila.Tekuila(key, cap, ratio)
        tekq.fetch_data()
        if tekq.check_cap() or tekq.check_warn():
            print "[WARNING] Threshold exceeded, pausing downloads."
            server.pausedownload()
        else:
            print "[DETAIL] Under threshold, no actions needed."

        return True

if __name__ == "__main__":
    schedulerscript = TekuilaGet()
    exit(schedulerscript.run())
