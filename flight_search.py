from os import environ
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class FlightSearch:
    """
    Searches the data of the flight
    """
    def __init__(self):
        self.AMADEUS_TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.AMADEUS_CITY_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        self.AMADEUS_PRICE_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        self.AMADEUS_API_KEY = environ["AMADEUS_API_KEY"]
        self.AMADEUS_API_SECRET = environ["AMADEUS_API_SECRET"]
        self.token = self.get_new_token()

    def get_new_token(self):
        """
        Gets a new token to use the Amadeus API
        More info: https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/API-Keys/authorization/
        :return:
        """
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

    def get_destination_data(self, city_name : str):
        """
        Gets the destination data
        More info: https://developers.amadeus.com/self-service/category/destination-experiences/api-doc/city-search/api-reference
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
            url=self.AMADEUS_CITY_ENDPOINT,
            headers=headers,
            params=parameters
        )

        # Tries to get the iataCode, in case if it exists.
        try:
            return response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"No airport code found for {city_name}")
            return "N/A"
        except KeyError:
            print(f"No airport code found for {city_name}")
            return "Not found"

    def check_flights(self, origin_city_code: str, destination_city_code : str, currency_code : str, is_direct : bool = True):
        """
        Gets the price data of flights using the Amadeus API
        More info: https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference
        :param origin_city_code: String with the code of the user's city
        :param destination_city_code: String with the code of the destination city
        :param currency_code: String with the currency  code
        :param is_direct: Boolean with code where it will only look flights that go from the origin
        :return:
        """
        tomorrow = datetime.today() + timedelta(days=1)
        tomorrow = tomorrow.strftime("%Y-%m-%d")

        # Headers with the token data
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        parameters = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": tomorrow,
            "adults": 1,
            "nonStop": is_direct,
            "currencyCode": currency_code
        }

        response = requests.get(
            url=self.AMADEUS_PRICE_ENDPOINT,
            headers=headers,
            params=parameters
        )

        return  response.json()