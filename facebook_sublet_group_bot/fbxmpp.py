import sleekxmpp
import logging

logging.basicConfig(level=logging.FATAL)


# Based on what I learned here:
# http://goo.gl/oV5KtZ
# Slightly updated since some parts didn't work
class SendMsgBot(sleekxmpp.ClientXMPP):

    """
    A basic SleekXMPP bot that will log in, send a message,
    and then log out.
    """

    def __init__(self, jid, recipient, message):

        sleekxmpp.ClientXMPP.__init__(self, jid, 'ignore')

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start, threaded=True)

    def start(self, event):

        self.send_presence()

        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        # Using wait=True ensures that the send queue will be
        # emptied before ending the session.
        self.disconnect(wait=True)
