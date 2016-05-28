"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa
from noaa import Noaa

HOME_STATION = 'MTR'

def lambda_handler(request_obj, context=None):
    '''
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {}
    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="NOAA launched")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="NOAA signoff")

@alexa.intent_handler("DiscussionIntent")
def discussion_intent_handler(request):
    report = Noaa()
    station= self.HOME_STATION
    report.get_afd_for(station)

    if report.error:
        card_title = 'error'
        content = 'Sorry. {}'.format(report.error)
    else:
        card_title = 'activated'
        content = report.sections['DISCUSSION']
    
    card = alexa.create_card(title = 'DiscussionIntent {}'.format(card_title),  subtitle='Station: {}'.format(station), content=content)
    return alexa.create_response(content, end_session=True, card_obj = card)

