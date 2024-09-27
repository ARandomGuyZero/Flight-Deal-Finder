class FlightData:
    """
    Separates the data in order to find the cheapest flight
    """
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

def find_cheapest_flight(data):
    """
    Gets a list with every flight available towards each destination
    :param data:
    :return:
    """
    # Handle empty data if no flight or Amadeus rate limit exceeded
    if data is None or not data['data']:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    # Data from the first flight in the json
    first_flight = data['data'][0]
    # A flight with 2 segments will have 1 stop
    nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1
    # Lowest flight found
    lowest_price = float(first_flight["price"]["grandTotal"])
    # Origin of the flight
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    # Destination of the flight
    destination = first_flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
    # Date the flight starts
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    # Date the flight will return
    return_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]

    # Initialize FlightData with the first flight for comparison
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)

    # For each flight in the data, we get the necessary data from the json file
    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)
            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight