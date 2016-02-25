from bottle import route
from passivetotal.libs.actions import ActionsClient
from ptxforms import load_maltego
from ptxforms.common.response import error_response
from ptxforms.common.response import maltego_response
from ptxforms.common.utilities import safe_symbols
# const
from ptxforms.common.const import MALTEGO_PHRASE
from ptxforms.common.const import MALTEGO_PT_TAG
from ptxforms.common.maltego import UIM_INFORM
# routes
from ptxforms.common.routes import ROUTE_ADD_TAGS
from ptxforms.common.routes import ROUTE_GET_CLASSIFICATION
from ptxforms.common.routes import ROUTE_GET_COMPROMISED
from ptxforms.common.routes import ROUTE_GET_DYNAMIC_DNS
from ptxforms.common.routes import ROUTE_GET_MONITOR
from ptxforms.common.routes import ROUTE_GET_SINKHOLE
from ptxforms.common.routes import ROUTE_GET_TAGS
from ptxforms.common.routes import ROUTE_SET_MALICIOUS
from ptxforms.common.routes import ROUTE_SET_NON_MALICIOUS
from ptxforms.common.routes import ROUTE_SET_SUSPICIOUS
from ptxforms.common.routes import ROUTE_SET_UNKNOWN


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
        return ActionsClient(username, api_key, server, version)
    else:
        return ActionsClient(username, api_key)


@route(ROUTE_GET_TAGS, method="ANY")
@load_maltego(debug=False)
def get_tags(trx, context):
    """Get tags for query value."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_tags(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    for tag in response.get('tags', []):
        trx.addEntity(MALTEGO_PT_TAG, safe_symbols(tag))
    return maltego_response(trx)


@route(ROUTE_ADD_TAGS, method="ANY")
@load_maltego(debug=False)
def add_tags(trx, context):
    """Add tags to query value."""
    query_value = context.Value
    client = load_client(context)
    raw_tags = context.getProperty('tags')
    tags = [x.strip() for x in raw_tags.split(',')]
    response = client.add_tags(query=query_value, tags=tags)
    if 'error' in response:
        return error_response(trx, response)

    trx.addUIMessage("PassiveTotal tagging successful", UIM_INFORM)
    return maltego_response(trx)


@route(ROUTE_GET_CLASSIFICATION, method="ANY")
@load_maltego(debug=False)
def get_classification(trx, context):
    """Get classification for query value."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_classification_status(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    content = response.get('classification', 'N/A')
    trx.addEntity(MALTEGO_PHRASE, safe_symbols(content))
    return maltego_response(trx)


@route(ROUTE_GET_COMPROMISED, method="ANY")
@load_maltego(debug=False)
def get_ever_compromised(trx, context):
    """Get ever-compromised for query value."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_ever_compromised_status(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    content = "Unknown"
    if response.get('everCompromised', False):
        content = "Been Compromised"
    trx.addEntity(MALTEGO_PHRASE, safe_symbols(content))
    return maltego_response(trx)


@route(ROUTE_GET_SINKHOLE, method="ANY")
@load_maltego(debug=False)
def get_sinkhole(trx, context):
    """Get sinkhole for query value."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_sinkhole_status(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    content = "Unknown"
    if response.get('sinkhole', False):
        content = "Sinkholed"
    trx.addEntity(MALTEGO_PHRASE, safe_symbols(content))
    return maltego_response(trx)


@route(ROUTE_GET_DYNAMIC_DNS, method="ANY")
@load_maltego(debug=False)
def get_dynamic_dns(trx, context):
    """Get dynamic-dns for query value."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_dynamic_dns_status(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    content = "Unknown"
    if response.get('dynamicDns', False):
        content = "Dynamic DNS"
    trx.addEntity(MALTEGO_PHRASE, safe_symbols(content))
    return maltego_response(trx)


@route(ROUTE_GET_MONITOR, method="ANY")
@load_maltego(debug=False)
def get_monitor(trx, context):
    """Get monitor status for query value."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_monitor_status(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    content = "Unknown"
    if response.get('monitor', False):
        content = "Monitoring"
    trx.addEntity(MALTEGO_PHRASE, safe_symbols(content))
    return maltego_response(trx)


def abstract_classification(trx, context, classification):
    """Abstraction for setting classifications."""
    query_value = context.Value
    client = load_client(context)
    response = client.set_classification_status(
        query=query_value,
        classification=classification
    )
    if 'error' in response:
        return error_response(trx, response)

    trx.addUIMessage("PassiveTotal classification successful", UIM_INFORM)
    return maltego_response(trx)


@route(ROUTE_SET_MALICIOUS, method="ANY")
@load_maltego(debug=False)
def set_classification_malicious(trx, context):
    """Set classification for query value."""
    return abstract_classification(trx, context, "malicious")


@route(ROUTE_SET_SUSPICIOUS, method="ANY")
@load_maltego(debug=False)
def set_classification_suspicious(trx, context):
    """Set classification for query value."""
    return abstract_classification(trx, context, "suspicious")


@route(ROUTE_SET_NON_MALICIOUS, method="ANY")
@load_maltego(debug=False)
def set_classification_non_malicious(trx, context):
    """Set classification for query value."""
    return abstract_classification(trx, context, "non-malicious")


@route(ROUTE_SET_UNKNOWN, method="ANY")
@load_maltego(debug=False)
def set_classification_unknown(trx, context):
    """Set classification for query value."""
    return abstract_classification(trx, context, "unknown")
