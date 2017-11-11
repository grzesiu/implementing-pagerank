from collections import defaultdict


class PR:
    def __init__(self, airports, routes, df=0.9):
        self.airports = airports
        self.routes = routes
        self.df = df

    def compute_page_ranks(self):
        pass

    def __str__(self):
        return str(self.routes)[:1000] + '\n' + str(self.airports)

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
            iata = temp[4][1:-1]
            if iata:
                name = temp[2][1:-1]
                airports[iata] = name

        return airports

    @staticmethod
    def read_routes(routes_as_str):
        routes = defaultdict(lambda: defaultdict(float))
        out_degs = defaultdict(float)
        for line in routes_as_str:
            temp = line.split(',')
            origin = temp[2]
            destination = temp[4]
            routes[destination][origin] += 1
            out_degs[origin] += 1

        for destination in routes:
            for origin in routes[destination]:
                routes[destination][origin] /= out_degs[origin]

        return routes


def main():
    with open("airports.txt", "r") as f:
        airports_as_str = f.readlines()
    with open("test_routes.txt", "r") as f:
        routes_as_str = f.readlines()

    pr = PR.from_str(airports_as_str, routes_as_str)
    print(pr)


if __name__ == "__main__":
    main()
