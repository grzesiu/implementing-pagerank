from collections import defaultdict


class PR:
    def __init__(self, airports, routes, df=0.9):
        self.airports = airports
        self.routes = routes
        self.df = df

    def compute_page_ranks(self):
        q = {i: 1 / len(self.airports) for i in self.airports}

        while True:
            print("dupa")
            p = dict(q)
            for destination in self.routes:
                q[destination] = \
                    self.df \
                    * sum([weight * p[origin] for origin, weight in self.routes[destination].items()]) \
                    + (1 - self.df) / len(self.airports)

            if self.stop(p, q, 1e-10):
                return q

    @staticmethod
    def stop(p, q, precision):
        for k in p.keys():
            if q[k] + precision > p[k] > q[k] - precision:
                return True
        return False

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
    with open("test_airports.txt", "r") as f:
        airports_as_str = f.readlines()
    with open("test_routes.txt", "r") as f:
        routes_as_str = f.readlines()

    pr = PR.from_str(airports_as_str, routes_as_str)
    print(pr.compute_page_ranks())


if __name__ == "__main__":
    main()
