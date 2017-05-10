import networkx

graph = networkx.Graph()
graph.add_edge("New York", "San Francisco", weight=2908)
graph.add_edge("San Francisco", "Los Angeles", weight=382)
graph.add_edge("Los Angeles", "New York", weight=2776)
graph.add_edge("San Francisco", "Portland", weight=635)

print networkx.shortest_path(graph, "New York", "Portland")

