from collections import deque
from heapq import heappush, heappop


# I worked with Mikey on this lab
def shortest_shortest_path(graph, source):
    """
    Params:
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node

    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    # From Professor Ding's Class notes
    def dijkstra_helper(visited, frontier):
        if len(frontier) == 0:
            return visited
        else:
            # Pick next closest node from heap
            distance, num_edges, node = heappop(frontier)
            #print('visiting', node)
            if node in visited:
                # Already visited, so ignore this longer path
                return dijkstra_helper(visited, frontier)
            else:
                # We now know the shortest path from source to node.
                # insert into visited dict.
                visited[node] = (distance, num_edges)
                #print(visited)
                #print('...weight=', distance, "distance = ", num_edges)
                # Visit each neighbor of node and insert into heap.
                # We may add same node more than once, heap
                # will keep shortest distance prioritized.
                for neighbor, weight in graph[node]:
                    heappush(frontier, (distance + weight, num_edges + 1, neighbor))
                return dijkstra_helper(visited, frontier)

    frontier = []
    heappush(frontier, (0, 0, source))
    visited = dict()  # store the final shortest paths for each node.
    #print(frontier)
    return dijkstra_helper(visited, frontier)


def test_shortest_shortest_path():
    graph = {
        's': {('a', 1), ('c', 4)},
        'a': {('b', 2)},  # 'a': {'b'},
        'b': {('c', 1), ('d', 4)},
        'c': {('d', 3)},
        'd': {},
        'e': {('d', 0)}
    }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0, 0)
    assert result['a'] == (1, 1)
    assert result['b'] == (3, 2)
    assert result['c'] == (4, 1)
    assert result['d'] == (7, 2)


def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of
      that vertex in the shortest path tree.
    """
    result = {}
    frontier = {source}

    while len(frontier) > 0:
        next_source = frontier.pop()
        for node in graph[next_source]:
            if node[0] not in result.keys():
                result[node[0]] = next_source
                frontier.add(node[0])

    return result


def get_sample_graph():
    return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }


def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'


def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node
      (excluding the destination node itself). See test_get_path for an example.
    """
    res = ""
    if destination in parents.keys():
        res = parents[destination] + res
        res = get_path(parents, parents[destination]) + res
    return res


def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    get_path(parents, 'd') == 'sbc'
