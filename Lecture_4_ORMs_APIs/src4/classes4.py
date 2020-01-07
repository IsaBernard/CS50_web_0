class Flight:

    counter = 1

    def __init__(self, origin, destination, duration):

        # Keep track of id number. Not declared in __init__.
        # Will give an automatic id to any new object of class Flight, based on the value of counter then add 1.
        self.id = Flight.counter
        Flight.counter += 1

        # Keep track of passengers. Not declared in __init__.
        self.passengers = []

        # Details about flight.
        self.origin = origin
        self.destination = destination
        self.duration = duration

    def print_info(self):
        print(f"Flight origin: {self.origin}")
        print(f"Flight destination: {self.destination}")
        print(f"Flight duration: {self.duration}")

        print()
        print("Passengers:")
        for passenger in self.passengers:
            print(f"{passenger.name}")

    def delay(self, amount):
        self.duration += amount

    # append to the list self.passengers passenger p for flight id
    def add_passenger(self, p):
        self.passengers.append(p)
        p.flight_id = self.id


class Passenger:

    def __init__(self, name):
        self.name = name


def main():

    # Create flight.
    f1 = Flight(origin="New York", destination="Paris", duration=540)

    # Create passengers.
    alice = Passenger(name="Alice")
    bob = Passenger("Bob")

    # Add passengers.
    f1.add_passenger(alice)
    f1.add_passenger(bob)

    f1.print_info()


if __name__ == "__main__":
    main()
