import os
import sys

sys.path = ['/opt/passivetotal/integrations/maltego_tds_transforms/ptxforms/', '/opt/passivetotal/integrations/maltego_tds_transforms/'] + sys.path
os.chdir(os.path.dirname(__file__))

from ptxforms.common.const import MALTEGO_COUNTRY
from ptxforms.common.const import MALTEGO_DOMAIN
from ptxforms.common.const import MALTEGO_EMAIL
from ptxforms.common.const import MALTEGO_IP
from ptxforms.common.const import MALTEGO_PHRASE
from ptxforms.common.const import MALTEGO_PT_COMPONENT
from ptxforms.common.const import MALTEGO_PT_NAMESERVER
from ptxforms.common.const import MALTEGO_PT_SSL_CERT
from ptxforms.common.const import MALTEGO_URL

import ptxforms.common.routes as const

test_spec = {
    const.ROUTE_GET_TAGS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_ADD_TAGS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org', 'tags': 'testing'}
    },
    const.ROUTE_GET_CLASSIFICATION: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_COMPROMISED: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_SINKHOLE: {
        'types': [MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_DYNAMIC_DNS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_URL],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_MONITOR: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_SET_MALICIOUS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_SET_SUSPICIOUS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_SET_NON_MALICIOUS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_SET_UNKNOWN: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_ATTRIBUTE_COMPONENTS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP,
                  MALTEGO_URL, MALTEGO_PT_COMPONENT],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_ENRICHMENT: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP, MALTEGO_URL],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_OSINT: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP, MALTEGO_URL],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_OSINT_DETAILS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP, MALTEGO_URL],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_SUBDOMAINS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP, MALTEGO_URL],
        'params': {'query': '*.passivetotal.org'}
    },
    const.ROUTE_GET_WHOIS: {
        'types': [MALTEGO_DOMAIN, MALTEGO_PHRASE, MALTEGO_URL],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_SEARCH_WHOIS_DOMAIN: {
        'types': [MALTEGO_DOMAIN, MALTEGO_PHRASE],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_SEARCH_WHOIS_EMAIL: {
        'types': [MALTEGO_EMAIL, MALTEGO_PHRASE],
        'params': {'query': 'admin@passivetotal.org'}
    },
    const.ROUTE_SEARCH_WHOIS_NAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'Brandon Dixon'}
    },
    const.ROUTE_SEARCH_WHOIS_ORGANIZATION: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'PassiveTotal'}
    },
    const.ROUTE_SEARCH_WHOIS_ADDRESS: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'United States'}
    },
    const.ROUTE_SEARCH_WHOIS_PHONE: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': '1800'}
    },
    const.ROUTE_SEARCH_WHOIS_NAMESERVER: {
        'types': [MALTEGO_DOMAIN, MALTEGO_URL, MALTEGO_PHRASE,
                  MALTEGO_PT_NAMESERVER],
        'params': {'query': 'ns1.digitalocean.com'}
    },
    const.ROUTE_GET_PASSIVE: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP, MALTEGO_URL],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_UNIQUE_PASSIVE: {
        'types': [MALTEGO_DOMAIN, MALTEGO_IP, MALTEGO_URL],
        'params': {'query': 'passivetotal.org'}
    },
    const.ROUTE_GET_SSL: {
        'types': [MALTEGO_PHRASE, MALTEGO_PT_SSL_CERT],
        'params': {'query': 'e9a6647d6aba52dc47b3838c920c9ee59bad7034'}
    },
    const.ROUTE_GET_SSL_HISTORY_IP: {
        'types': [MALTEGO_IP],
        'params': {'query': '52.8.228.23'}
    },
    const.ROUTE_GET_SSL_HISTORY_SHA1: {
        'types': [MALTEGO_PHRASE, MALTEGO_PT_SSL_CERT],
        'params': {'query': 'e9a6647d6aba52dc47b3838c920c9ee59bad7034'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_COMMONNAME: {
        'types': [MALTEGO_PHRASE, MALTEGO_DOMAIN],
        'params': {'query': 'www.passivetotal.org'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_COUNTRY: {
        'types': [MALTEGO_PHRASE, MALTEGO_COUNTRY],
        'params': {'query': 'US'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_EMAILADDRESS: {
        'types': [MALTEGO_EMAIL, MALTEGO_PHRASE],
        'params': {'query': 'admin@passivetotal.org'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_GIVENNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'PassiveTotal'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_LOCALITYNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'San Francisco'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_ORGANIZATIONNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'PassiveTotal'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_ORGANIZATIONUNITNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'Operations'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_PROVINCE: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'San Francisco'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_SERIALNUMBER: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': '92938'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_STATEORPROVINCENAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'San Francisco'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_STREETADDRESS: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': '22 Battery St'}
    },
    const.ROUTE_SEARCH_SSL_ISSUER_SURNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    },
    const.ROUTE_SEARCH_SSL_SERIALNUMBER: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': '92938'}
    },
    const.ROUTE_SEARCH_SSL_SSLVERSION: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': '200'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_COMMONNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'www.riskiq.net'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_COUNTRY: {
        'types': [MALTEGO_PHRASE, MALTEGO_COUNTRY],
        'params': {'query': 'US'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_EMAILADDRESS: {
        'types': [MALTEGO_EMAIL],
        'params': {'query': '92938'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_GIVENNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_LOCALITYNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'San Francisco'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_ORGANIZATIONNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ, Inc.'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_ORGANIZATIONUNITNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'Operations'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_PROVINCE: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'San Francisco'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_SERIALNUMBER: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': '92938'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_STATEORPROVINCENAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'San Francisco'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_STREETADDRESS: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': '22 Battery St.'}
    },
    const.ROUTE_SEARCH_SSL_SUBJECT_SURNAME: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    },
    const.ROUTE_SEARCH_TRACKERS_CLICKY: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    },
    const.ROUTE_SEARCH_TRACKERS_NEW_RELIC: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    },
    const.ROUTE_SEARCH_TRACKERS_GOOGLE_ACCOUNT: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    },
    const.ROUTE_SEARCH_TRACKERS_GOOGLE_ANALYTICS: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    },
    const.ROUTE_SEARCH_TRACKERS_MIXPANEL: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    },
    const.ROUTE_SEARCH_TRACKERS_YANDEX: {
        'types': [MALTEGO_PHRASE],
        'params': {'query': 'RiskIQ'}
    }
}

testdata = list()
for key, value in test_spec.iteritems():
    for item in value.get('types', []):
        tmp = (key, {'entity': item, 'params': value['params']})
        testdata.append(tmp)
        print key, item
