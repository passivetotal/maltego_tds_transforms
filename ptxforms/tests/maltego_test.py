import logging
import pytest
import requests
from xml.dom import minidom
from ptxforms.tests import testdata

# Use local values for testing
API_USERNAME = 'brandon@passivetotal.org'
API_KEY = 'c6c877fc8e2761dc6f1b0dc8cf485cc6924bedf8e144921353d4dbb7c839b25c'
API_SERVER = "127.0.0.1"
API_VERSION = "v2"
TEST_LOCAL = True
MALTEGO_SERVER = "http://%s:8443" % (API_SERVER)


def build_maltego_response(context):
    """Build a valid maltego response that emulates the clinent."""
    content = ''
    content += '<?xml version="1.0" encoding="UTF-8"?><root>'
    content += '<Value>%s</Value>' % context.get('params').get('query', '')
    content += '<Weight>0</Weight>'
    content += '<Entity Type="%s"></Entity>' % context.get('entity')
    content += '<Limits SoftLimit="100"></Limits>'
    content += '<TransformFields>'
    content += '<Field Name="username">%s</Field>' % API_USERNAME
    content += '<Field Name="aKey">%s</Field>' % API_KEY
    content += '<Field Name="test_local">%s</Field>' % str(TEST_LOCAL)
    content += '<Field Name="server">%s</Field>' % API_SERVER
    content += '<Field Name="version">%s</Field>' % API_VERSION
    content += '</TransformFields>'
    content += '<AdditionalFields>'
    for name, value in context.get('params', {}).iteritems():
        if name == 'query':
            continue
        content += '<Field Name="%s">%s</Field>' % (name, value)
    content += '</AdditionalFields>'
    content += '</root>'
    return content


@pytest.mark.parametrize("endpoint,details", testdata)
def test_valid_calls(endpoint, details):
    """Test all endpoints with valid calls."""
    full_url = MALTEGO_SERVER + endpoint
    logging.debug("Requesting %s" % full_url)
    response = requests.post(
        full_url,
        data=build_maltego_response(details),
        auth=(API_USERNAME, API_KEY),
        verify=False
    )
    logging.debug("Response %s" % response.content)
    assert response.status_code == 200
    xmldoc = minidom.parseString(response.content)
    messages = xmldoc.getElementsByTagName('UIMessage')
    for message in messages:
        value = message.attributes['MessageType'].value
        assert value != 'FatalError'