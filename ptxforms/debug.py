import bottle
# specific
from beaker.middleware import SessionMiddleware

import ptxforms.actions
import ptxforms.attributes
import ptxforms.dns
import ptxforms.enrichment
import ptxforms.ssl
import ptxforms.whois


class Webserver():

    """Abstract our webserver so its outside the core app folder."""

    def __init__(self, host, port):
        # associate the session to our app
        local_app = SessionMiddleware(bottle.app())

        bottle.run(
            app=local_app,
            server='cherrypy',
            host=host,
            port=port,
            reloader=True
        )
