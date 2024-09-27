"""
Flight Deal Finder

Author: Alan
Date: September 26th 2024

This script gets the price data of flights.
"""

from data_manager import DataManager
from flight_search import FlightSearch

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