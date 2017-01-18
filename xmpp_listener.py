import sleekxmpp
from slack_message_client import SlackMessageClient

'''
Stripped down extention of ClientXMPP.
'''
class XmppListener(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, messaging_client):
        super(XmppListener, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.slack_client = messaging_client

    def start(self, start):
        startup_payload = self.slack_client.build_payload("Listener started.", None)
        self.slack_client.send_message(startup_payload)

    def message(self, msg):
        attachment = self.slack_client.build_attachment(
            "pleaseignore.com",
            "#D00000",
            "",
            msg['body']
            )
        payload = self.slack_client.build_payload("", attachment)

        # Post Slack Message
        self.slack_client.send_message(payload)
