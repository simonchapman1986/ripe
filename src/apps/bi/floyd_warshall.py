"""
Example of Floyd-Warshall Algorithm
@author: Simon Chapman

Introduction:

Floyd-Warshall is a very simple, but inefficient shortest path algorithm that has O(V3) time complexity. Based on the
two dimensional matrix of the distances between nodes, this algorithm finds out the shortest distance between each and
every pair of nodes.

Pseudocode:

    Given a set of nodes and their distances, it is required to find the shortest path between two chosen nodes
    (Node1, Node2)
    If a distance between two nodes is not provided, set the distance as a really huge number (ex 999999999) to
    make sure that the nodes are disconnected.
    For each and every possible combination of three nodes (A, B, C):
    Compare distance of A-B + B-C with A-C.
    If A-B+B-C is shorter than A-C, replace the distance of A-C with A-B+B-C in the matrix.
    The resulting matrix states the shortest distance between two nodes and if the distance is equal or bigger
    than the huge number (999999999), the nodes are disconnected.

Practical example: lets say there are five cities: A, B, C, D, E

Distances:

    AB: 50
    AC: 200
    AD: 300
    AE: Disconnected
    BC: 300
    BD: Disconnected
    BE: 100
    CD: 80
    CE: 500
    DE: 100

We want to find the shortest distance between A and E (currently disconnected)

There are many possible paths:

    AB - BE
    AC - CE
    AD - DE
    AB - BC - CE
    and more

To determine the shortest path, we use Floyd-Warshall Algorithm described above
"""

def floyd_warshall(path_map, numNode):
    """
    >>> hugeNumber = 999999999  # a really huge number for disconnected cities
    >>> dist = (\
        [0, 50, 200, 300, hugeNumber],\
        [50, 0, 300, hugeNumber, 100],\
        [200, 300, 0, 80, 500],\
        [300, hugeNumber, 80, 0, 100],\
        [hugeNumber, 100, 500, 100, 0]\
    )
    >>> numNode = len(dist)
    >>> print('Before Distance AE: %d'%dist[4][0])
    Before Distance AE: 999999999
    >>> dist = floyd_warshall(path_map=dist, numNode=numNode)
    >>> print('After Distance AE: %d'%dist[4][0])
    After Distance AE: 150
    """
    for i in range(numNode):
        for j in range(numNode):
            for k in range(numNode):
                path_map[i][k] = min(path_map[i][k],path_map[i][j]+path_map[j][k])
 
    return path_map
 

 
