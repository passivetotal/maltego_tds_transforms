from bottle import request
from ptxforms.common.maltego import MaltegoMsg
from ptxforms.common.maltego import MaltegoTransform
# import logging
# logging.basicConfig(level=logging.DEBUG)


def load_maltego(debug=False):
    """Decorator that will validate the presence of specific fields."""
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            body = request.body.getvalue()
            # logging.debug("Body: %s" % str(body))
            maltego = MaltegoMsg(body)
            trx = MaltegoTransform()
            return func(trx, maltego, *args, **kwargs)
        return wrapper
    return real_decorator
