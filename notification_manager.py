from os import environ
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

class NotificationManager:
    """
    This sends a notification when a price of a flight has gone lower.
    """
    def __init__(self):
        self.TWILIO_ACCOUNT_SID = environ["TWILIO_ACCOUNT_SID"]
        self.AUTH_TOKEN = environ["AUTH_TOKEN"]
        self.TWILIO_PHONE = environ["TWILIO_PHONE"]
        self.YOUR_PHONE = environ["YOUR_PHONE"]

    def send_message(self, message_body: str):
        """
        Uses the twilio library to send a message via SMS
        :return:
        """
        client = Client(self.TWILIO_ACCOUNT_SID, self.AUTH_TOKEN)

        client.messages.create(
            body=message_body,
            from_=self.TWILIO_PHONE,
            to=self.YOUR_PHONE,
        )