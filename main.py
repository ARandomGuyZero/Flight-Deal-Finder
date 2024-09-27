"""
Flight Deal Finder

Author: Alan
Date: September 26th 2024

This script gets the price data of flights.
"""

from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

ORIGIN_COUNTRY_CODE = "MEX"
CURRENCY_CODE = "MXM"

data_manager = DataManager() # New object class with the data from the worksheet
flight_search = FlightSearch() # New object class with the data from the flight
notification_manager = NotificationManager()

# Set it to a new variable
sheet_data = data_manager.get_destination_data()

# For each row (list) of the sheet data, we will replace the iataCode in the variable
for row in sheet_data:

    if row["iataCode"] == "":

        row["iataCode"] = flight_search.get_destination_data(row["city"])

# Replace the old data with the new data
data_manager.destination_data = sheet_data

# Update the data in the code
data_manager.put_destination_data()

# Get a list of data with the user's email
customer_data = data_manager.get_user_email_data()

customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]

for destination in sheet_data:

    # Get data using flight
    flights = flight_search.check_flights(
        origin_city_code=ORIGIN_COUNTRY_CODE,
        currency_code=CURRENCY_CODE,
        destination_city_code=destination["iataCode"],
        is_direct=False
    )

    # Get the cheapest flight data
    cheapest_flight = find_cheapest_flight(flights)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")

        message_body = f"Low price alert! Only £{cheapest_flight.price} to fly "
        f'from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, '
        f'on {cheapest_flight.out_date} until {cheapest_flight.return_date}.'

        # Sends a message to the phone number
        notification_manager.send_message(
            message_body=message_body
        )

        # Sends an email to the users
        for email in customer_email_list:
            notification_manager.send_email(
                user_email=email,
                message_body=message_body
            )