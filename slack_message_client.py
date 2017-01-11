import requests
import json

class SlackMessageClient(object):
    def __init__(self, url, TOKEN, CHANNEL):
        self.url_endpoint = url
        self.SLACK_TOKEN = TOKEN
        self.SLACK_CHANNEL = CHANNEL

    def build_payload(self, text, attachment):
        if attachment is None: 
            return {
                "token" : self.SLACK_TOKEN,
                "channel" : self.SLACK_CHANNEL,
                "text" : text
            }
        else:
            return {
                "token" : self.SLACK_TOKEN,
                "channel" : self.SLACK_CHANNEL,
                "attachments" : attachment,
            }

    def build_attachment(self, pretext, color, title, value):
        return json.dumps([{
            "fallback" : pretext,
            "pretext" : pretext,
            "color" : color,
            "fields" : [{
                "title" : title,
                "value" : value
                }]
            }])
    
    def send_message(self, payload):
        # attachment = self.build_attachment("another test", "#D00000", "once more", "for good measure")
        # attachment = None
        # payload = self.build_payload("", attachment)
        # payload = self.build_payload("blah", attachment)
        r = requests.post(self.url_endpoint, payload)
        if(r.status_code != 200):
            print"ERROR sending ping to Slack!"
