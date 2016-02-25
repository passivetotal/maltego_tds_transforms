from bottle import route
from passivetotal.libs.ssl import SslRequest
from ptxforms import load_maltego
from ptxforms.common.response import error_response
from ptxforms.common.response import maltego_response
from ptxforms.common.response import blank_response
from ptxforms.common.utilities import safe_symbols
from ptxforms.common.utilities import upper_first
# const
from ptxforms.common.const import MALTEGO_IP
from ptxforms.common.const import MALTEGO_PT_SSL_CERT
from ptxforms.common.const import LABEL_FIRST_SEEN
from ptxforms.common.const import LABEL_LAST_SEEN
from ptxforms.common.const import LABEL_PROPERTY
# routes
from ptxforms.common.routes import ROUTE_GET_SSL
from ptxforms.common.routes import ROUTE_GET_SSL_HISTORY_IP
from ptxforms.common.routes import ROUTE_GET_SSL_HISTORY_SHA1
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_COMMONNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_COUNTRY
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_EMAILADDRESS
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_GIVENNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_LOCALITYNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_ORGANIZATIONNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_ORGANIZATIONUNITNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_PROVINCE
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_SERIALNUMBER
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_STATEORPROVINCENAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_STREETADDRESS
from ptxforms.common.routes import ROUTE_SEARCH_SSL_ISSUER_SURNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SERIALNUMBER
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SSLVERSION
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_COMMONNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_COUNTRY
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_EMAILADDRESS
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_GIVENNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_LOCALITYNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_ORGANIZATIONNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_ORGANIZATIONUNITNAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_PROVINCE
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_SERIALNUMBER
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_STATEORPROVINCENAME
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_STREETADDRESS
from ptxforms.common.routes import ROUTE_SEARCH_SSL_SUBJECT_SURNAME

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
        return SslRequest(username, api_key, server, version)
    else:
        return SslRequest(username, api_key)


@route(ROUTE_GET_SSL, method="ANY")
@load_maltego(debug=False)
def get_ssl_certificate_details(trx, context):
    """Get SSL certificate data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_ssl_certificate_details(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    for entity, value in response.iteritems():
        if value == '' or not value:
            continue
        entity_name = "pt.ssl%s" % upper_first(entity)
        ent = trx.addEntity(entity_name, safe_symbols(value))
        ent.addProperty(LABEL_PROPERTY, LABEL_PROPERTY,
                        'loose', upper_first(entity))

    return maltego_response(trx)


@route(ROUTE_GET_SSL_HISTORY_IP, method="ANY")
@load_maltego(debug=False)
def get_ssl_certificate_history_by_ip(trx, context):
    """Get unique passive DNS data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_ssl_certificate_history(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    for item in response.get('results', []):
        ent = trx.addEntity(MALTEGO_PT_SSL_CERT,
                            safe_symbols(item.get('sha1')))
        ent.addProperty(LABEL_FIRST_SEEN, LABEL_FIRST_SEEN,
                        'loose', safe_symbols(item.get('firstSeen', 'N/A')))
        ent.addProperty(LABEL_LAST_SEEN, LABEL_LAST_SEEN,
                        'loose', safe_symbols(item.get('lastSeen', 'N/A')))

    return maltego_response(trx)


@route(ROUTE_GET_SSL_HISTORY_SHA1, method="ANY")
@load_maltego(debug=False)
def get_ssl_certificate_history_by_ip(trx, context):
    """Get unique passive DNS data."""
    query_value = context.Value
    client = load_client(context)
    response = client.get_ssl_certificate_history(query=query_value)
    if 'error' in response:
        return error_response(trx, response)

    for item in response.get('results', []):
        for ip_address in item.get('ipAddresses'):
            ent = trx.addEntity(MALTEGO_IP,
                                safe_symbols(ip_address))
            ent.addProperty(LABEL_FIRST_SEEN, LABEL_FIRST_SEEN,
                            'loose', safe_symbols(item.get('firstSeen', 'N/A')))
            ent.addProperty(LABEL_LAST_SEEN, LABEL_LAST_SEEN,
                            'loose', safe_symbols(item.get('lastSeen', 'N/A')))

    return maltego_response(trx)


def run_ssl_certificate_search(trx, context, field):
    """Abstract runner to search certificate data."""
    query_value = context.Value
    client = load_client(context)
    response = client.search_ssl_certificate_by_field(
        query=query_value,
        field=field
    )
    if 'error' in response:
        return error_response(trx, response)

    results = response.get('results', [])
    if len(results) == 0:
        return blank_response(trx, response)

    for item in results:
        trx.addEntity(MALTEGO_PT_SSL_CERT, safe_symbols(item.get('sha1')))

    return maltego_response(trx)


@route(ROUTE_SEARCH_SSL_ISSUER_COMMONNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_commonName(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerCommonName")


@route(ROUTE_SEARCH_SSL_ISSUER_COUNTRY, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_country(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerCountry")


@route(ROUTE_SEARCH_SSL_ISSUER_EMAILADDRESS, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_emailAddress(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerEmailAddress")


@route(ROUTE_SEARCH_SSL_ISSUER_GIVENNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_givenName(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerGivenName")


@route(ROUTE_SEARCH_SSL_ISSUER_LOCALITYNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_localityName(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerLocalityName")


@route(ROUTE_SEARCH_SSL_ISSUER_ORGANIZATIONNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_organizationName(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerOrganizationName")


@route(ROUTE_SEARCH_SSL_ISSUER_ORGANIZATIONUNITNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_organizationUnitName(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerOrganizationUnitName")


@route(ROUTE_SEARCH_SSL_ISSUER_PROVINCE, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_province(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerProvince")


@route(ROUTE_SEARCH_SSL_ISSUER_SERIALNUMBER, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_serialNumber(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerSerialNumber")


@route(ROUTE_SEARCH_SSL_ISSUER_STATEORPROVINCENAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_stateOrProvinceName(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerStateOrProvinceName")


@route(ROUTE_SEARCH_SSL_ISSUER_STREETADDRESS, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_streetAddress(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerStreetAddress")


@route(ROUTE_SEARCH_SSL_ISSUER_SURNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_issuer_surname(trx, context):
    return run_ssl_certificate_search(trx, context, "issuerSurname")


@route(ROUTE_SEARCH_SSL_SERIALNUMBER, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_serialNumber(trx, context):
    return run_ssl_certificate_search(trx, context, "serialNumber")


@route(ROUTE_SEARCH_SSL_SSLVERSION, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_sslVersion(trx, context):
    return run_ssl_certificate_search(trx, context, "sslVersion")


@route(ROUTE_SEARCH_SSL_SUBJECT_COMMONNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_commonName(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectCommonName")


@route(ROUTE_SEARCH_SSL_SUBJECT_COUNTRY, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_country(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectCountry")


@route(ROUTE_SEARCH_SSL_SUBJECT_EMAILADDRESS, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_emailAddress(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectEmailAddress")


@route(ROUTE_SEARCH_SSL_SUBJECT_GIVENNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_givenName(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectGivenName")


@route(ROUTE_SEARCH_SSL_SUBJECT_LOCALITYNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_localityName(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectLocalityName")


@route(ROUTE_SEARCH_SSL_SUBJECT_ORGANIZATIONNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_organizationName(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectOrganizationName")


@route(ROUTE_SEARCH_SSL_SUBJECT_ORGANIZATIONUNITNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_organizationUnitName(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectOrganizationUnitName")


@route(ROUTE_SEARCH_SSL_SUBJECT_PROVINCE, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_province(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectProvince")


@route(ROUTE_SEARCH_SSL_SUBJECT_SERIALNUMBER, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_serialNumber(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectSerialNumber")


@route(ROUTE_SEARCH_SSL_SUBJECT_STATEORPROVINCENAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_stateOrProvinceName(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectStateOrProvinceName")


@route(ROUTE_SEARCH_SSL_SUBJECT_STREETADDRESS, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_streetAddress(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectStreetAddress")


@route(ROUTE_SEARCH_SSL_SUBJECT_SURNAME, method="ANY")
@load_maltego(debug=False)
def ssl_search_by_subject_surname(trx, context):
    return run_ssl_certificate_search(trx, context, "subjectSurname")
