import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

with open('chic_choc_data.csv') as f:
    for line in f:
        v1, v2 = line.strip().split(',')
        G.add_node(v1)
        G.add_node(v2)
        G.add_edge(v1, v2)

print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

