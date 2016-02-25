import sys
from ptxforms.debug import Webserver

if len(sys.argv) == 2:
    debug = True
else:
    debug = False

Webserver('0.0.0.0', 8443)
