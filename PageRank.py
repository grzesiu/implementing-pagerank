from collections import defaultdict
import operator
import time


class PR:
    def __init__(self, airports, routes, df, precision):
        self.airports = airports
        self.routes = routes
        self.df = df
        self.precision = precision

    def compute_page_ranks(self):
        # at first q is dict of airport codes as keys and 1/n as values
        q = {i: 1 / len(self.airports) for i in self.airports}

        # iteration counter
        k = 0
        while True:
            # p is a copy of q so that changing p wouldn't change q
            p = dict(q)
            for destination in self.airports:
                # apply pageRank
                q[destination] = \
                    self.df \
                    * sum([weight * p[origin] for origin, weight in self.routes[destination].items()]) \
                    + (1 - self.df) / len(self.airports)

            # check if iteration values already too similar
            if self.stop(p, q):
                return PR.norm(q)

            k += 1

    def stop(self, p, q):
        for k in p.keys():
            if q[k] + self.precision > p[k] and p[k] > q[k] - self.precision:
                return True
        return False

    @classmethod
    def create(cls, airports_as_str, routes_as_str, df, precision):
        airports = cls.read_airports(airports_as_str)
        routes = cls.read_routes(routes_as_str)

        airports = PR.add_missing(routes, airports, "NO_NAME")
        routes = PR.add_missing(airports, routes, defaultdict(float))

        return cls(airports, routes, df, precision)

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

    @staticmethod
    def add_missing(from_dict, to_dict, default):
        missing = {k: default for k in set(from_dict) - set(to_dict)}
        return {**to_dict, **missing}

    @staticmethod
    def norm(p):
        return {k: v / sum(p.values()) for k, v in p.items()}


def main():
    with open("airports.txt", "r", encoding="utf8") as f:
        airports_as_str = f.readlines()
    with open("routes.txt", "r", encoding="utf8") as f:
        routes_as_str = f.readlines()

    pr = PR.create(airports_as_str, routes_as_str, 2/3, 1e-5)
    # measuring pageRank elapsed time
    start_time = time.time()
    try_count = 10
    for i in range(10):
        ranks = (pr.compute_page_ranks())
    print("Elapsed time: " + str((time.time() - start_time)/try_count))
    # if sum of probabilities equals to one then the pageRank vector is done right
    prob_sum = (sum(pr.compute_page_ranks().values()))

    sorted_x = list(reversed(sorted(ranks.items(), key=operator.itemgetter(1))))
    with open("output.txt", mode='w', encoding="utf8") as f:
        # [print(str(element[1]) + ", " + pr.airports[str(element[0])]) for element in sorted_x]
        [f.write(str(element[1]) + ", " + pr.airports[str(element[0])] + "\n") for element in sorted_x]


if __name__ == "__main__":
    main()
