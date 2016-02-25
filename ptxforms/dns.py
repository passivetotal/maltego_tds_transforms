from bottle import route
from passivetotal.libs.dns import DnsRequest
from ptxforms import load_maltego
from ptxforms.common.response import error_response
from ptxforms.common.response import maltego_response
from ptxforms.common.utilities import safe_symbols
# const
from ptxforms.common.const import MALTEGO_IP
from ptxforms.common.const import MALTEGO_DOMAIN
from ptxforms.common.const import LABEL_FIRST_SEEN
from ptxforms.common.const import LABEL_LAST_SEEN
from ptxforms.common.const import LABEL_SOURCES
# routes
from ptxforms.common.routes import ROUTE_GET_PASSIVE
from ptxforms.common.routes import ROUTE_GET_PASSIVE_WITH_TIME
from ptxforms.common.routes import ROUTE_GET_UNIQUE_PASSIVE


# import logging
# logging.basicConfig(level=logging.DEBUG)

type_map = {
    'ip': MALTEGO_DOMAIN,
    'domain': MALTEGO_IP
}


def load_client(context):
    """Get an instance of a loaded client."""
    username = context.getTransformSetting('username')
    api_key = context.getTransformSetting('aKey')
    test_status = context.getTransformSetting('test_local')
    if test_status and test_status == 'True':
        server = context.getTransformSetting('server')
        version = context.getTransformSetting('version')
        return DnsRequest(username, api_key, server, version)
    else:
        return DnsRequest(username, api_key)


@route(ROUTE_GET_PASSIVE, method="ANY")
@load_maltego(debug=False)
def get_passive_dns(trx, context):
    """Get passive DNS data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_passive_dns(query=query_value, timeout=10)
    if 'error' in response:
        return error_response(trx, response)

    query_type = response.get('queryType')
    for item in response.get('results', []):
        resolution = item.get('resolve', 'N/A')
        ent = trx.addEntity(type_map[query_type], safe_symbols(resolution))
        ent.addProperty(LABEL_FIRST_SEEN, LABEL_FIRST_SEEN,
                        'loose', safe_symbols(item.get('firstSeen', 'N/A')))
        ent.addProperty(LABEL_LAST_SEEN, LABEL_LAST_SEEN,
                        'loose', safe_symbols(item.get('lastSeen', 'N/A')))
        ent.addProperty(LABEL_SOURCES, LABEL_SOURCES, 'loose',
                        safe_symbols(', '.join(item.get('source', []))))

    return maltego_response(trx)


@route(ROUTE_GET_PASSIVE_WITH_TIME, method="ANY")
@load_maltego(debug=False)
def get_passive_dns_with_time(trx, context):
    """Get passive DNS data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_passive_dns(query=query_value, timeout=10)
    if 'error' in response:
        return error_response(trx, response)

    query_type = response.get('queryType')
    for item in response.get('results', []):
        resolution = item.get('resolve', 'N/A')
        ent = trx.addEntity(type_map[query_type], safe_symbols(resolution))
        ent.addProperty(LABEL_FIRST_SEEN, LABEL_FIRST_SEEN,
                        'loose', safe_symbols(item.get('firstSeen', 'N/A')))
        ent.addProperty(LABEL_LAST_SEEN, LABEL_LAST_SEEN,
                        'loose', safe_symbols(item.get('lastSeen', 'N/A')))
        ent.addProperty(LABEL_SOURCES, LABEL_SOURCES, 'loose',
                        safe_symbols(', '.join(item.get('source', []))))

        first_seen = safe_symbols(item.get('firstSeen', 'N/A'))
        last_seen = safe_symbols(item.get('lastSeen', 'N/A'))
        time_period = "%s - %s" % (first_seen, last_seen)
        ent.setLinkLabel(time_period)

    return maltego_response(trx)


@route(ROUTE_GET_UNIQUE_PASSIVE, method="ANY")
@load_maltego(debug=False)
def get_unique_passive_dns(trx, context):
    """Get unique passive DNS data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_unique_resolutions(query=query_value, timeout=10)
    if 'error' in response:
        return error_response(trx, response)

    query_type = response.get('queryType')
    for item in response.get('results', []):
        trx.addEntity(type_map[query_type], safe_symbols(item))

    return maltego_response(trx)
