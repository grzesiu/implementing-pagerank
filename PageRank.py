import argparse
import time
from collections import defaultdict


class PR:
    def __init__(self, airports, routes, sinks, df, precision):
        self.airports = airports
        self.routes = routes
        self.sinks = sinks
        self.df = df
        self.precision = precision

    def compute_page_ranks(self):
        q = {i: 1 / len(self.airports) for i in self.airports}
        k = 0
        n = len(self.airports)
        while True:
            k += 1
            p = dict(q)

            p_sinks = sum(p[sink] for sink in self.sinks) / n

            for destination in self.airports:
                q[destination] = \
                    self.df \
                    * (p_sinks + sum([weight * p[origin] for origin, weight in self.routes[destination].items()])) \
                    + (1 - self.df) / n

            # sum of probabilities is equal to 1 in all iterations
            # print(sum(q.values()))

            if self.stop(p, q):
                return q, k

    def stop(self, p, q):
        for k in p.keys():
            if q[k] + self.precision > p[k] > q[k] - self.precision:
                return True
        return False

    @classmethod
    def create(cls, airports_as_str, routes_as_str, df, precision):
        airports = cls.read_airports(airports_as_str)
        routes, sinks = cls.read_routes(routes_as_str, airports)

        return cls(airports, routes, sinks, df, precision)

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
    def read_routes(routes_as_str, airports):
        routes = defaultdict(lambda: defaultdict(float))
        out_degs = defaultdict(float)
        for line in routes_as_str:
            temp = line.split(',')
            origin = temp[2]
            destination = temp[4]

            # we are adding only routes between airports that are present in the airports database
            if origin in airports and destination in airports:
                routes[destination][origin] += 1
                out_degs[origin] += 1

        for destination in routes:
            for origin in routes[destination]:
                routes[destination][origin] /= out_degs[origin]

        sinks = set(airports.keys()) - set(out_degs.keys())
        return routes, sinks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--airports', default='airports.txt', help='Airports file')
    parser.add_argument('--routes', default='routes.txt', help='Routes file')
    parser.add_argument('--output', default='out.csv', help='Output file')
    parser.add_argument('--precision', default=1e-12, type=float, help='Precision that the results have to converge to')
    parser.add_argument('--df', default=0.8, type=float, help='Dumping factor')

    args = parser.parse_args()

    with open(args.airports, "r", encoding="utf8") as f:
        airports_as_str = f.readlines()
    with open(args.routes, "r", encoding="utf8") as f:
        routes_as_str = f.readlines()

    pr = PR.create(airports_as_str, routes_as_str, args.df, args.precision)

    start_time = time.time()

    result, k = pr.compute_page_ranks()

    end_time = time.time()

    print("Number of vertices:", len(pr.airports))
    print("Number of vertices with no outgoing edges:", len(pr.sinks))
    print("Number of edges:", sum(len(v) for v in pr.routes.values()))
    print("Number of iterations:", k)
    print("Time of calculating PageRanks:", end_time - start_time)
    print("Results saved to:", args.output)
    with open(args.output, 'w') as f:
        for k in result.keys():
            f.write('{},{},{}\n'.format(k, pr.airports[k], result[k]))


if __name__ == "__main__":
    main()
