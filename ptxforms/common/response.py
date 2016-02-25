from bottle import HTTPResponse
# const
from ptxforms.common.const import MALTEGO_PHRASE
from ptxforms.common.maltego import UIM_FATAL
from ptxforms.common.maltego import UIM_INFORM


def format_error(response):
    """Format the error to be sent back to the user.

    :param response: API response back from PassiveTotal
    """
    error = response.get('error', dict())
    message = ("PassiveTotal: [HTTP %d] %s, %s" % (
        error.get('http_code', 500),
        error.get('message', 'Failed to grab message'),
        error.get('developer_message', 'Failed to grab message')
    ))

    return message


def maltego_response(trx, status_code=200):
    """Return a properly formatted Maltego response."""
    response = trx.returnOutput()
    return HTTPResponse(status=status_code, body=response)


def error_response(trx, response):
    """Single output flow for returning an error.

    :param response: API response back from PassiveTotal
    """
    trx.addUIMessage(format_error(response), UIM_FATAL)
    if response['error'].get('http_code', 500) == 401:
        # HTTP code for Maltego mis-matched authentication
        status_code = 406
    elif response['error'].get('http_code', 500) == 403:
        # Avoid popping a direct error and return a phrase
        ent = trx.addEntity(MALTEGO_PHRASE, "Daily Query Limit Reached")
        ent.setNote("Looks like you ran out of queries for the day. These "
                    "limits are reset on a daily basis and can be removed with"
                    " an enteprise account. For more details, email"
                    " feedback@passivetotal.org or visit "
                    "https://www.passivetotal.org/enterprise")
        status_code = 200
    else:
        status_code = 500

    return maltego_response(trx, status_code=status_code)


def blank_response(trx, response):
    """Single output flow for returning a blank message.

    :param response: API response back from PassiveTotal
    """
    trx.addUIMessage("No results found", UIM_INFORM)
    return maltego_response(trx)
