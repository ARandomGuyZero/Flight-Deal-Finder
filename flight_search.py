from os import environ

import requests
from dotenv import load_dotenv

load_dotenv()

class FlightSearch:
    """
    Searches the data of the flight
    """
    def __init__(self):
        self.AMADEUS_TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.AMADEUS_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"

        self.AMADEUS_API_KEY = environ["AMADEUS_API_KEY"]
        self.AMADEUS_API_SECRET = environ["AMADEUS_API_SECRET"]
        self.token = self.get_new_token()

    def get_new_token(self):

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        body = {
            "grant_type": "client_credentials",
            "client_id": self.AMADEUS_API_KEY,
            "client_secret": self.AMADEUS_API_SECRET,
        }

        response = requests.post(
            url=self.AMADEUS_TOKEN_ENDPOINT,
            headers=headers,
            data=body,
        )

        return response.json()["access_token"]

    def get_destination_data(self, city_name):
        """
        Gets the destination data
        :param city_name: String with the name of the city
        :return:
        """
        # Headers with the token
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        parameters = {
            "keyword": city_name,
            "max": 1,
            "include": "AIRPORTS"
        }

        response = requests.get(
            url=self.AMADEUS_ENDPOINT,
            headers=headers,
            params=parameters
        )

        # Tries to get the iataCode, in case if it exists.
        try:
            return response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"No airport code found for: {city_name}")
            return "N/A"
        except KeyError:
            print(f"No airport code found for {city_name}")
            return "Not found"