from collections import defaultdict
import re
import sys


def route(graph, start):
    dist = defaultdict(lambda: len(graph))
    prev = defaultdict(lambda: None)
    visited = set()

    dist[start] = 0
    q = {start: 0}

    while q:
        (nn, d) = sorted(q.items(), key=lambda p: p[1])[0]
        del q[nn]
        visited.add(nn)
        for vn in graph[nn]['edges']:
            if vn in visited:
                continue
            alt = d + 1
            if alt < dist[vn]:
                dist[vn] = alt
                q[vn] = alt
                prev[vn] = nn
    return dist, prev    


def load_graph(filename):
    graph = {}

    with open(filename, 'rt') as input_file:
        pat = re.compile('^Valve (?P<name>[^ ]+)[^=]+=(?P<rate>[^;]+);.*valves? (?P<cons>.*)')
        for line in input_file:
            m = pat.search(line.strip())
            d = m.groupdict()
            graph[d['name']] = {
                'name': d['name'],
                'rate': int(d['rate']),
                'edges': [v.strip() for v in d['cons'].split(',')],
            }

    return graph


if __name__ == "__main__":
    graph = load_graph(sys.argv[1])

    time = 30
    total = 0
    opened = []
    starts = {'AA'}.union([k for k,v in graph.items() if v['rate'] > 0])
    print(starts)
    routes = {k: route(graph, k) for k in starts}
    starts.remove('AA')

    start = 'AA'
    while True:
        opening = []
        dist, prev = routes[start]
        dpdt = {k: graph[k]['rate']/(2*dist[k] + 1) for k in starts}
        dt = 1
        if dpdt:
            print(sorted(dpdt.items(), key=lambda t: t[1], reverse=True))
            k, dpdtx = sorted(dpdt.items(), key=lambda t: t[1], reverse=True)[0]
            dt = dist[k] + 1
            opening = [k]
            starts.remove(k)
            start = k
        for v in opened:
            total += dt*graph[v]['rate']
        opened.extend(opening)
        time -= dt
        if time <= 0:
            break

    print(time)
    print(opened)
    print(total)