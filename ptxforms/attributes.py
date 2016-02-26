from bottle import request
from bottle import route
from passivetotal.libs.attributes import AttributeRequest
from ptxforms import load_maltego
from ptxforms.common.response import blank_response
from ptxforms.common.response import error_response
from ptxforms.common.response import maltego_response
from ptxforms.common.utilities import gen_debug
from ptxforms.common.utilities import safe_symbols
# const
from ptxforms.common.const import LABEL_BLACKLISTED
from ptxforms.common.const import LABEL_COMPONENT_TYPE
from ptxforms.common.const import LABEL_FIRST_SEEN
from ptxforms.common.const import LABEL_HOSTNAME
from ptxforms.common.const import LABEL_LAST_SEEN
from ptxforms.common.const import LABEL_TRACKER_TYPE
from ptxforms.common.const import MALTEGO_DOMAIN
from ptxforms.common.const import MALTEGO_PT_COMPONENT
# routes
from ptxforms.common.routes import ROUTE_GET_ATTRIBUTE_COMPONENTS
from ptxforms.common.routes import ROUTE_GET_ATTRIBUTE_TRACKERS
from ptxforms.common.routes import ROUTE_SEARCH_TRACKERS_CLICKY
from ptxforms.common.routes import ROUTE_SEARCH_TRACKERS_GOOGLE_ACCOUNT
from ptxforms.common.routes import ROUTE_SEARCH_TRACKERS_GOOGLE_ANALYTICS
from ptxforms.common.routes import ROUTE_SEARCH_TRACKERS_MIXPANEL
from ptxforms.common.routes import ROUTE_SEARCH_TRACKERS_NEW_RELIC
from ptxforms.common.routes import ROUTE_SEARCH_TRACKERS_YANDEX

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
        return AttributeRequest(username, api_key, server, version)
    else:
        return AttributeRequest(username, api_key, headers=gen_debug(request))


@route(ROUTE_GET_ATTRIBUTE_TRACKERS, method="ANY")
@load_maltego(debug=False)
def get_host_attribute_trackers(trx, context):
    """Get tracker data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_host_attribute_trackers(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    results = response.get('results', [])
    if len(results) == 0:
        return blank_response(trx, response)

    for item in results:
        entity_name = "pt.tracker%s" % item.get('attributeType')
        ent = trx.addEntity(entity_name,
                            safe_symbols(item.get('attributeValue')))
        ent.addProperty(LABEL_FIRST_SEEN, LABEL_FIRST_SEEN,
                        'loose', safe_symbols(item.get('firstSeen', 'N/A')))
        ent.addProperty(LABEL_LAST_SEEN, LABEL_LAST_SEEN,
                        'loose', safe_symbols(item.get('lastSeen', 'N/A')))
        ent.addProperty(LABEL_TRACKER_TYPE, LABEL_LAST_SEEN,
                        'loose', safe_symbols(item.get('attributeType')))
        ent.addProperty(LABEL_HOSTNAME, LABEL_HOSTNAME,
                        'loose', safe_symbols(item.get('hostname')))

    return maltego_response(trx)


@route(ROUTE_GET_ATTRIBUTE_COMPONENTS, method="ANY")
@load_maltego(debug=False)
def get_host_attribute_components(trx, context):
    """Get component data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_host_attribute_components(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    results = response.get('results', [])
    if len(results) == 0:
        return blank_response(trx, response)

    for item in results:
        entity_value = "%s (%s)" % (item.get('label'), item.get('category'))
        ent = trx.addEntity(MALTEGO_PT_COMPONENT, safe_symbols(entity_value))
        ent.addProperty(LABEL_FIRST_SEEN, LABEL_FIRST_SEEN,
                        'loose', safe_symbols(item.get('firstSeen', 'N/A')))
        ent.addProperty(LABEL_LAST_SEEN, LABEL_LAST_SEEN,
                        'loose', safe_symbols(item.get('lastSeen', 'N/A')))
        ent.addProperty(LABEL_COMPONENT_TYPE, LABEL_LAST_SEEN,
                        'loose', safe_symbols(item.get('category')))
        ent.addProperty(LABEL_HOSTNAME, LABEL_HOSTNAME,
                        'loose', safe_symbols(item.get('hostname')))

    return maltego_response(trx)


def run_tracker_search(trx, context, field):
    """Abstract runner to search tracker data."""
    query_value = context.Value
    client = load_client(context)
    response = client.search_trackers(query=query_value, type=field)
    if 'error' in response:
        return error_response(trx, response)

    results = response.get('results', [])
    if len(results) == 0:
        return blank_response(trx, response)

    for item in results:
        ent = trx.addEntity(MALTEGO_DOMAIN, safe_symbols(item.get('hostname')))
        ent.addProperty(LABEL_BLACKLISTED, LABEL_BLACKLISTED,
                        'loose', safe_symbols(item.get('everBlacklisted',)))

    return maltego_response(trx)


@route(ROUTE_SEARCH_TRACKERS_GOOGLE_ACCOUNT, method="ANY")
@load_maltego(debug=False)
def get_tracker_search_by_google_account(trx, context):
    return run_tracker_search(trx, context, 'GoogleAnalyticsAccountNumber')


@route(ROUTE_SEARCH_TRACKERS_YANDEX, method="ANY")
@load_maltego(debug=False)
def get_tracker_search_by_yandex(trx, context):
    return run_tracker_search(trx, context, 'YandexMetricaCounterId')


@route(ROUTE_SEARCH_TRACKERS_GOOGLE_ANALYTICS, method="ANY")
@load_maltego(debug=False)
def get_tracker_search_by_google_analytics(trx, context):
    return run_tracker_search(trx, context, 'GoogleAnalyticsTrackingId')


@route(ROUTE_SEARCH_TRACKERS_NEW_RELIC, method="ANY")
@load_maltego(debug=False)
def get_tracker_search_by_new_relic(trx, context):
    return run_tracker_search(trx, context, 'NewRelicId')


@route(ROUTE_SEARCH_TRACKERS_MIXPANEL, method="ANY")
@load_maltego(debug=False)
def get_tracker_search_by_mixpanel(trx, context):
    return run_tracker_search(trx, context, 'MixpanelId')


@route(ROUTE_SEARCH_TRACKERS_CLICKY, method="ANY")
@load_maltego(debug=False)
def get_tracker_search_by_clicky(trx, context):
    return run_tracker_search(trx, context, 'ClickyId')
