import heapq

def prim_mst(graph):
    # Choose starting vertex
    start = list(graph.keys())[0]
    
    visited = set()
    min_heap = [(0, start)]   # (weight, vertex)
    total_cost = 0
    mst = []

    while min_heap:
        weight, vertex = heapq.heappop(min_heap)

        if vertex in visited:
            continue

        visited.add(vertex)
        total_cost += weight

        for neighbor, edge_weight in graph[vertex]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, neighbor))
                mst.append((vertex, neighbor, edge_weight))

    return total_cost, mst


# Example Graph (Adjacency List)
graph = {
    'A': [('B', 2), ('C', 3)],
    'B': [('A', 2), ('C', 1), ('D', 4)],
    'C': [('A', 3), ('B', 1), ('D', 5)],
    'D': [('B', 4), ('C', 5)]
}

cost, edges = prim_mst(graph)

print("Minimum Spanning Tree Cost:", cost)
print("Edges in MST:")
for edge in edges:
    print(edge)
