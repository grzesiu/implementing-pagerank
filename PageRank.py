from collections import defaultdict


class PR:
    def __init__(self, airports, routes):
        self.airports = airports
        self.routes = routes

    def compute_page_ranks(self):
        pass

    def __str__(self):
        return str(self.airports) + '\n' + str(self.routes)

    @classmethod
    def from_str(cls, airports_as_str, routes_as_str):
        airports = cls.read_airports(airports_as_str)
        routes = cls.read_routes(routes_as_str)
        return cls(airports, routes)

    @staticmethod
    def read_airports(airports_as_str):
        airports = {}

        for line in airports_as_str:
            temp = line.split(',')
            name = temp[2][1:-1]
            iata = temp[4][1:-1]
            if iata:
                airports[iata] = name

        return airports

    @staticmethod
    def read_routes(routes_as_str):
        routes = defaultdict(lambda: defaultdict(int))

        for line in routes_as_str:
            temp = line.split(',')
            origin = temp[2]
            destination = temp[4]
            routes[origin][destination] += 1

        return routes


def main():
    with open("airports.txt", "r") as f:
        airports_as_str = f.readlines()
    with open("routes.txt", "r") as f:
        routes_as_str = f.readlines()

    pr = PR.from_str(airports_as_str, routes_as_str)
    print(pr)


if __name__ == "__main__":
    main()
