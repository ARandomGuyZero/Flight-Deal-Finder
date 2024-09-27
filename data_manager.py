from os import environ
from requests import get, put
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    """
    Uses the Sheety API to add a row
    For some info: https://sheety.co/docs
    User might not use AUTH_USER neither AUTH_PASSWORD
    """
    def __init__(self):
        self.SHEETY_WORKSHEET_ENDPOINT = environ["SHEETY_WORKSHEET_ENDPOINT"]
        self.AUTH_USER = environ["AUTH_USER"]
        self.AUTH_PASSWORD = environ["AUTH_PASSWORD"]
        self.destination_data = {}

    def get_destination_data(self):
        """
        Gets the destination data from the Google's Drive worksheet
        :return:
        """

        # Make a request to get the data of the worksheet
        response = get(
            url=self.SHEETY_WORKSHEET_ENDPOINT,
            auth=(
                self.AUTH_USER,
                self.AUTH_PASSWORD,
            )
        )

        # Store the data so we can work on it later
        self.destination_data = response.json()["prices"]

        # Return the data to work with it
        return self.destination_data

    def put_destination_data(self):
        """
        Puts the new data of the worksheet to the worksheet
        :return:
        """
        for city in self.destination_data:

            # Data we will update in the destination_data
            parameters = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }

            # Make a request to put the new data to the worksheet
            response = put(
                url=f"{self.SHEETY_WORKSHEET_ENDPOINT}/{city["id"]}",
                json=parameters,
                auth=(
                    self.AUTH_USER,
                    self.AUTH_PASSWORD,
                )
            )

            # Print the data
            print(response.text)