from os import environ
from dotenv import load_dotenv
from twilio.rest import Client
from smtplib import SMTP

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

        self.EMAIL = environ["EMAIL"]
        self.PASSWORD = environ["PASSWORD"]
        self.HOST = environ["HOST"]
        self.PORT = int(environ["PORT"])

    def send_message(self, message_body: str):
        """
        Uses the twilio library to send a message via SMS
        :param message_body: Message of the body
        :return:
        """
        client = Client(self.TWILIO_ACCOUNT_SID, self.AUTH_TOKEN)

        client.messages.create(
            body=message_body,
            from_=self.TWILIO_PHONE,
            to=self.YOUR_PHONE,
        )

    def send_email(self, user_email, message_body):
        with SMTP(host=self.HOST, port=self.PORT) as connection:

            connection.starttls()

            connection.login(user=self.EMAIL, password=self.PASSWORD)

            connection.sendmail(from_addr=self.EMAIL, to_addrs=user_email, msg=f"Subject:New flight offer\n\n{message_body}")