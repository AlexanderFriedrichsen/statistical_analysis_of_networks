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

edges=[]
nodes =[]
with open(file_name, 'r') as file:
    for line in file:
        node = int(line.split(' ')[0])
        node_name = line.split(' ')[1].strip(',')
        nodes.append((node,node_name))
        l_ = line.split('[')[1]
        l_ = l_[1:-2].replace(', ', ',').strip().split(' ')
        for i in l_:
            if i != '':
                i = i.strip('(').strip(')').split(',')[0]
                edges.append((node,int(i)))

g = nx.Graph()
for node in nodes:
    g.add_node(node[0], label=node[1])
for edge in edges:
    g.add_edge(edge[0], edge[1])

pos = nx.spring_layout(g, k=0.15, iterations=50)
nx.draw(g, pos, with_labels=True, font_size=10, node_size=200, alpha=0.7, width=1, edge_color='grey', node_color='lightblue')
labels = nx.get_node_attributes(g,'label')
nx.draw_networkx_labels(g, pos, labels, font_size=8, font_weight='bold', alpha=0.8, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round, pad=0.3'))
edge_labels = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels, font_size=8, label_pos=0.5, font_color='grey', alpha=0.8)

plt.tight_layout()
plt.show()
