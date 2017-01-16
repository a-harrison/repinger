#!/usr/bin/env python

import sys
import logging
import getpass
from optparse import OptionParser
import json
import os
import ConfigParser
from slack_message_client import SlackMessageClient
from xmpp_listener import XmppListener

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

config = ConfigParser.ConfigParser();
config.read('./app.config');

SLACK_ENDPOINT_URL= "https://slack.com/api/chat.postMessage"

# Read configuration variables
SLACK_TOKEN = config.get('Configuration', 'SLACK_TOKEN')
SLACK_CHANNEL = config.get('Configuration', 'SLACK_CHANNEL')
XMPP_JID = config.get('Configuration', 'XMPP_JID')
XMPP_PASSWORD = config.get('Configuration', 'XMPP_PASSWORD')

if __name__ == '__main__':

    # Here we will configure and read command line options
    optp = OptionParser()
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)

    optp.add_option("-j", "--jid", dest="jid", help="JID to use")
    optp.add_option("-p", "--password", dest="password", help="password to use")
    opts, args = optp.parse_args()

    # Read from command line arguments if present.
    if opts.jid is not None:
        XMPP_JID = opts.jid
    if opts.password is not None:
        XMPP_PASSWORD = opts.password

    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

    # Setup slack integration
    messaging_client = SlackMessageClient(
        SLACK_ENDPOINT_URL,
        SLACK_TOKEN,
        SLACK_CHANNEL
       )

    # Here we will instantiate our echo bot
    if (XMPP_JID is None or XMPP_PASSWORD is None):
        print "Connection values not defined."
    else:
        xmpp = XmppListener(XMPP_JID, XMPP_PASSWORD, messaging_client)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0199') # Pings

        # Finally, we connect the bott and start listening for messages
        print "Connecting."
        if xmpp.connect():
            print "Connected!"
            xmpp.process(block=True)
        else:
            print('Unable to connect')
