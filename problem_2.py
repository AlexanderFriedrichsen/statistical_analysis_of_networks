import pandas as pd
import networkx as nx
import ast
import urllib.request
import zipfile
import matplotlib.pyplot as plt

url = 'http://aaronclauset.github.io/data/MediciNetwork.zip'
filename = 'MediciNetwork.zip'

# Download the file
urllib.request.urlretrieve(url, filename)

# Extract the contents of the zip file
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall('.')

file_name = 'Medici network/medici_network.txt'

edges = []
nodes = []
with open(file_name, 'r') as file:
    for line in file:
        node = int(line.split(' ')[0])
        node_name = line.split(' ')[1].strip(',')
        nodes.append((node, node_name))
        l_ = line.split('[')[1]
        l_ = l_[1:-2].replace(', ', ',').strip().split(' ')
        for i in l_:
            if i != '':
                i = i.strip('(').strip(')').split(',')[0]
                edges.append((node, int(i)))

g = nx.Graph()
for node in nodes:
    g.add_node(node[0], label=node[1])
for edge in edges:
    g.add_edge(edge[0], edge[1])

# Calculate harmonic centrality for each node
centrality = nx.harmonic_centrality(g, distance=None)
for node, value in centrality.items():
    if value == float('inf'):
        centrality[node] = 0

# Get node positions using spring layout
pos = nx.spring_layout(g)

# Draw graph with labels to the side
plt.figure(figsize=(10, 10))
nx.draw_networkx_nodes(g, pos, node_size=200, node_color=list(centrality.values()), cmap=plt.cm.Blues)
nx.draw_networkx_edges(g, pos, alpha=0.5)
label_pos = {k: [v[0]+0.03, v[1]+0.03] for k, v in pos.items()}  # Move labels to the side
nx.draw_networkx_labels(g, label_pos, labels=nx.get_node_attributes(g, 'label'), font_size=10)
plt.axis('off')
plt.savefig('HHHHmedici_network.png')
plt.show()
