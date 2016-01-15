__author__ = 'simon'


def edmonds_karp(C, source, sink):
    n = len(C) # C is the capacity matrix
    F = [[0] * n for i in xrange(n)]
    # residual capacity from u to v is C[u][v] - F[u][v]

    while True:
        path = bfs(C, F, source, sink)
        if not path:
            break
        # traverse path to find smallest capacity
        flow = min(C[u][v] - F[u][v] for u,v in path)
        # traverse path to update flow
        for u,v in path:
            F[u][v] += flow
            F[v][u] -= flow
    return sum(F[source][i] for i in xrange(n))


def bfs(C, F, source, sink):
    queue = [source]
    paths = {source: []}
    while queue:
        u = queue.pop(0)
        for v in xrange(len(C)):
            if C[u][v] - F[u][v] > 0 and v not in paths:
                paths[v] = paths[u] + [(u,v)]
                if v == sink:
                    return paths[v]
                queue.append(v)
    return None