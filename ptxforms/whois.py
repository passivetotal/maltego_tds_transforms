from bottle import route
from passivetotal.libs.whois import WhoisRequest
from ptxforms import load_maltego
from ptxforms.common.response import error_response
from ptxforms.common.response import maltego_response
from ptxforms.common.response import blank_response
from ptxforms.common.utilities import safe_symbols
from ptxforms.common.utilities import upper_first
# const
from ptxforms.common.const import MALTEGO_DOMAIN
from ptxforms.common.const import MALTEGO_PT_NAMESERVER
# routes
from ptxforms.common.routes import ROUTE_GET_WHOIS
from ptxforms.common.routes import ROUTE_SEARCH_WHOIS_ADDRESS
from ptxforms.common.routes import ROUTE_SEARCH_WHOIS_DOMAIN
from ptxforms.common.routes import ROUTE_SEARCH_WHOIS_EMAIL
from ptxforms.common.routes import ROUTE_SEARCH_WHOIS_NAME
from ptxforms.common.routes import ROUTE_SEARCH_WHOIS_NAMESERVER
from ptxforms.common.routes import ROUTE_SEARCH_WHOIS_ORGANIZATION
from ptxforms.common.routes import ROUTE_SEARCH_WHOIS_PHONE

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
        return WhoisRequest(username, api_key, server, version)
    else:
        return WhoisRequest(username, api_key)


@route(ROUTE_GET_WHOIS, method="ANY")
@load_maltego(debug=False)
def get_whois_details(trx, context):
    """Get WHOIS data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_whois_details(query=query_value, compact_record=True)
    if 'error' in response:
        return error_response(trx, response)

    nameservers = response.get('nameServers', [])
    for item in nameservers:
        trx.addEntity(MALTEGO_PT_NAMESERVER, safe_symbols(item))
    fields = ['registrar', 'registered', 'registryUpdatedAt', 'expiresAt']
    for item in fields:
        entity_name = "pt.whois%s" % upper_first(item)
        trx.addEntity(entity_name, safe_symbols(response.get(item)))
    trx.addEntity(MALTEGO_DOMAIN, safe_symbols(response.get('domain', '')))

    results = response.get('compact', {})
    for entity, value in results.iteritems():
        if len(value.get('raw', [])) == 0:
            continue
        entity_name = "pt.whois%s" % upper_first(entity)
        for item in value.get('raw', []):
            trx.addEntity(entity_name, safe_symbols(item))

    return maltego_response(trx)


def run_whois_search(trx, context, field):
    """Abstract runner to search whois data."""
    query_value = context.Value
    client = load_client(context)
    response = client.search_whois_by_field(query=query_value, field=field)
    if 'error' in response:
        return error_response(trx, response)

    results = response.get('results', [])
    if len(results) == 0:
        return blank_response(trx, response)

    for item in results:
        trx.addEntity(MALTEGO_DOMAIN, safe_symbols(item.get('domain')))

    return maltego_response(trx)


@route(ROUTE_SEARCH_WHOIS_DOMAIN, method="ANY")
@load_maltego(debug=False)
def get_whois_search_by_domain(trx, context):
    return run_whois_search(trx, context, 'domain')


@route(ROUTE_SEARCH_WHOIS_EMAIL, method="ANY")
@load_maltego(debug=False)
def get_whois_search_by_email(trx, context):
    return run_whois_search(trx, context, 'email')


@route(ROUTE_SEARCH_WHOIS_NAME, method="ANY")
@load_maltego(debug=False)
def get_whois_search_by_name(trx, context):
    return run_whois_search(trx, context, 'name')


@route(ROUTE_SEARCH_WHOIS_ORGANIZATION, method="ANY")
@load_maltego(debug=False)
def get_whois_search_by_organization(trx, context):
    return run_whois_search(trx, context, 'organization')


@route(ROUTE_SEARCH_WHOIS_ADDRESS, method="ANY")
@load_maltego(debug=False)
def get_whois_search_by_address(trx, context):
    return run_whois_search(trx, context, 'address')


@route(ROUTE_SEARCH_WHOIS_PHONE, method="ANY")
@load_maltego(debug=False)
def get_whois_search_by_phone(trx, context):
    return run_whois_search(trx, context, 'phone')


@route(ROUTE_SEARCH_WHOIS_NAMESERVER, method="ANY")
@load_maltego(debug=False)
def get_whois_search_by_nameserver(trx, context):
    return run_whois_search(trx, context, 'nameserver')
