import sys

routes = [
    "ssl_search_by_issuer_commonName",
    "ssl_search_by_issuer_country",
    "ssl_search_by_issuer_emailAddress",
    "ssl_search_by_issuer_givenName",
    "ssl_search_by_issuer_localityName",
    "ssl_search_by_issuer_organizationName",
    "ssl_search_by_issuer_organizationUnitName",
    "ssl_search_by_issuer_province",
    "ssl_search_by_issuer_serialNumber",
    "ssl_search_by_issuer_stateOrProvinceName",
    "ssl_search_by_issuer_streetAddress",
    "ssl_search_by_issuer_surname",
    "ssl_search_by_serialNumber",
    "ssl_search_by_sslVersion",
    "ssl_search_by_subject_commonName",
    "ssl_search_by_subject_country",
    "ssl_search_by_subject_emailAddress",
    "ssl_search_by_subject_givenName",
    "ssl_search_by_subject_localityName",
    "ssl_search_by_subject_organizationName",
    "ssl_search_by_subject_organizationUnitName",
    "ssl_search_by_subject_province",
    "ssl_search_by_subject_serialNumber",
    "ssl_search_by_subject_stateOrProvinceName",
    "ssl_search_by_subject_streetAddress",
    "ssl_search_by_subject_surname",
]

for route in routes:
    trimmed = route.replace('ssl_search_by_', '')
    const = "ROUTE_SEARCH_SSL_%s" % trimmed.upper()
    print '%s = "%s"' % (const, route)