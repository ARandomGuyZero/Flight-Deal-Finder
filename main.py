"""
Flight Deal Finder

Author: Alan
Date: September 26th 2024

This script gets the price data of flights.
"""
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from data_manager import DataManager

ORIGIN_COUNTRY_CODE = "MEX"
CURRENCY_CODE = "MXM"

data_manager = DataManager() # New object class with the data from the worksheet
flight_search = FlightSearch() # New object class with the data from the flight

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

for destination in sheet_data:

    # Get data using flightt
    flights = flight_search.check_flights(ORIGIN_COUNTRY_CODE, CURRENCY_CODE, destination["iataCode"])

    # Get the cheapest flight data
    cheapest_flight = find_cheapest_flight(flights)
