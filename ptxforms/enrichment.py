from bottle import request
from bottle import route
from passivetotal.libs.enrichment import EnrichmentRequest
from ptxforms import load_maltego
from ptxforms.common.response import error_response
from ptxforms.common.response import maltego_response
from ptxforms.common.utilities import gen_debug
from ptxforms.common.utilities import safe_symbols
from ptxforms.common.utilities import value_type
# const
from ptxforms.common.const import LABEL_LATITUDE
from ptxforms.common.const import LABEL_LONGITUDE
from ptxforms.common.const import MALTEGO_AS_NUMBER
from ptxforms.common.const import MALTEGO_DOMAIN
from ptxforms.common.const import MALTEGO_IP
from ptxforms.common.const import MALTEGO_LOCATION
from ptxforms.common.const import MALTEGO_NETBLOCK
from ptxforms.common.const import MALTEGO_PHRASE
from ptxforms.common.const import MALTEGO_PT_TAG
from ptxforms.common.const import MALTEGO_URL
from ptxforms.common.const import MALFORMITY_HASH
# routes
from ptxforms.common.routes import ROUTE_GET_ENRICHMENT
from ptxforms.common.routes import ROUTE_GET_MALWARE
from ptxforms.common.routes import ROUTE_GET_OSINT
from ptxforms.common.routes import ROUTE_GET_OSINT_DETAILS
from ptxforms.common.routes import ROUTE_GET_SUBDOMAINS

# import logging
# logging.basicConfig(level=logging.DEBUG)


def load_client(context):
    """Get an instance of a loaded client."""
    username = context.getTransformSetting('username')
    api_key = context.getTransformSetting('aKey')
    test_status = context.getTransformSetting('test_local')
    if test_status and test_status == 'True':
        server = context.getTransformSetting('server')
        version = context.getTransformSetting('version')
        return EnrichmentRequest(username, api_key, server, version)
    else:
        return EnrichmentRequest(username, api_key, headers=gen_debug(request))


@route(ROUTE_GET_ENRICHMENT, method="ANY")
@load_maltego(debug=False)
def get_enrichment(trx, context):
    """Get tracker data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_enrichment(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    query_type = response.get('queryType')
    if query_type == 'ip':
        as_number = response.get('autonomousSystemNumber')
        ent = trx.addEntity(MALTEGO_AS_NUMBER, safe_symbols(as_number))
        ent = trx.addEntity(MALTEGO_NETBLOCK,
                            safe_symbols(response.get('network')))
        as_name = response.get('autonomousSystemName')
        ent = trx.addEntity(MALTEGO_PHRASE, safe_symbols(as_name))
        ent = trx.addEntity(MALTEGO_LOCATION,
                            safe_symbols(response.get('country')))
        ent.addProperty(LABEL_LATITUDE, LABEL_LATITUDE, 'loose',
                        safe_symbols(response.get('latitude')))
        ent.addProperty(LABEL_LONGITUDE, LABEL_LONGITUDE, 'loose',
                        safe_symbols(response.get('longitude')))
        if response.get('sinkhole', False):
            trx.addEntity(MALTEGO_PHRASE, safe_symbols('Sinkholed'))
    else:
        trx.addEntity(MALTEGO_DOMAIN, safe_symbols(response.get('tld')))
        if response.get('dynamicDns', False):
            trx.addEntity(MALTEGO_PHRASE, safe_symbols('Dynamic DNS'))
        if response.get('primaryDomain', '') != query_type:
            trx.addEntity(MALTEGO_DOMAIN,
                          safe_symbols(response.get('primaryDomain')))

    if response.get('everCompromised', False):
        ent = trx.addEntity(MALTEGO_PHRASE, safe_symbols('Been compromised'))
    for tag in response.get('tags', []):
        ent = trx.addEntity(MALTEGO_PT_TAG, safe_symbols(tag))

    return maltego_response(trx)


@route(ROUTE_GET_OSINT, method="ANY")
@load_maltego(debug=False)
def get_osint(trx, context):
    """Get OSINT for a query."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_osint(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    for item in response.get('results', []):
        trx.addEntity(MALTEGO_PHRASE, safe_symbols(item.get('source')))
        trx.addEntity(MALTEGO_URL, safe_symbols(item.get('sourceUrl')))
        for tag in item.get('tags', []):
            trx.addEntity(MALTEGO_PT_TAG, safe_symbols(tag))

    return maltego_response(trx)


@route(ROUTE_GET_OSINT_DETAILS, method="ANY")
@load_maltego(debug=False)
def get_osint_details(trx, context):
    """Get OSINT for a query."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_osint(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    for item in response.get('results', []):
        for value in item.get('inReport', []):
            if value_type(value) == 'ip':
                trx.addEntity(MALTEGO_IP, safe_symbols(value))
            else:
                trx.addEntity(MALTEGO_DOMAIN, safe_symbols(value))

    return maltego_response(trx)


@route(ROUTE_GET_SUBDOMAINS, method="ANY")
@load_maltego(debug=False)
def get_subdomains(trx, context):
    """Get subdomains for a query."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_subdomains(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    for item in response.get('subdomains', []):
        entity_value = "%s.%s" % (item, query_value)
        trx.addEntity(MALTEGO_DOMAIN, safe_symbols(entity_value))

    return maltego_response(trx)


@route(ROUTE_GET_MALWARE, method="ANY")
@load_maltego(debug=False)
def get_malware(trx, context):
    """Get malware for a query."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_malware(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    for item in response.get('results', []):
        trx.addEntity(MALTEGO_PHRASE, safe_symbols(item.get('source')))
        trx.addEntity(MALTEGO_URL, safe_symbols(item.get('sourceUrl')))
        trx.addEntity(MALFORMITY_HASH, safe_symbols(item.get('sample')))

    return maltego_response(trx)
