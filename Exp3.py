import heapq

def prim_mst(graph):
    # Start at 'A'
    start_node = 'A'
    visited = set()
    
    # min_heap stores: (weight, current_node, from_node)
    min_heap = [(0, start_node, None)]
    
    total_cost = 0
    mst_edges = []

    while min_heap:
        weight, u, prev = heapq.heappop(min_heap)

        # CRITICAL: If we've already visited this node, 
        # this edge is a "loop" or redundant. Skip it.
        if u in visited:
            continue

        # Add to MST
        visited.add(u)
        total_cost += weight
        if prev is not None:
            mst_edges.append((prev, u, weight))

        # Check neighbors
        for v, edge_weight in graph[u]:
            if v not in visited:
                heapq.heappush(min_heap, (edge_weight, v, u))

    return total_cost, mst_edges

# 5-Vertex Graph (Adjacency List)
graph_5 = {
    'A': [('B', 2), ('D', 6)],
    'B': [('A', 2), ('C', 3), ('D', 8), ('E', 5)],
    'C': [('B', 3), ('E', 7)],
    'D': [('A', 6), ('B', 8), ('E', 9)],
    'E': [('B', 5), ('C', 7), ('D', 9)]
}

cost, mst = prim_mst(graph_5)

print(f"Total MST Cost: {cost}")
print("Final MST Edges:")
for edge in mst:
    print(f"{edge[0]} - {edge[1]} (Weight: {edge[2]})")
