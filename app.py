#!/usr/bin/env python

import sys
import logging
import getpass
from optparse import OptionParser
import json
import os 

# Dependencies
import sleekxmpp
import requests


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

slack_url= "https://slack.com/api/chat.postMessage"

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')

XMPP_JID = os.environ.get('XMPP_JID')
XMPP_PASSWORD = os.environ.get('XMPP_PASSWORD')
text = ""

class EchoBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        super(EchoBot, self).__init__(jid, password)

    self.add_event_handler('session_start', self.start)
    self.add_event_handler('message', self.message)

    def start(self, start):
        self.send_presence()
        self.get_roster()
        

    def message(self, msg):
        print "Type: %s" % msg['type']
        print "From: %s" % msg['from']
        print "To: %s" % msg['to']
        print "Body: %s" % msg['body']
        
        message = [{
            "fallback" : "pleaseignore.com: ",
            "pretext" : "pleaseignore.com: ",
            "color" : "#D00000",
            "fields" : [{
                "title" : "",
                "value" : msg['body']
                "short" : false
                }]
        }]
        
        attachment = json.dumps(message)
        
        payload = {
            'token' : SLACK_TOKEN,
            'channel' : SLACK_CHANNEL,
            'attachments' : attachment,
            'text' : text
        }

        # Post Slack Message
        r.requests.post(url, data=payload)
        if(r.status_code != 200):
            print "ERROR sending ping to Slack!"
            
                
if __name__ == '__main__':

    # Here we will configure and read command line options
    optp = OptionParser()
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)

    optp.add_option("-j", "--jid", dest="jid", help="JID to use")
    optp.add_option("-p", "--password", dest="password", help="password to use")
    opts, args = optp.parse_args()
    
    # if opts.jid is None:
    #     opts.jid = raw_input("Username: ")
    # if opts.password is None:
    #     opts.password = getpass.getpass("Password: ")

    if opts.jid is not None:
        XMPP_JID = opts.jid
    if opts.password is not None:
        XMPP_PASSWORD = opts.password    
    
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

    # Here we will instantiate our echo bot
    xmpp = EchoBot(XMPP_JID, XMPP_PASSWORD)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # Pings
    
    # Finally, we connect the bott and start listening for messages
    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect')