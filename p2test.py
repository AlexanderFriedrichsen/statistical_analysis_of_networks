import pandas as pd
import networkx as nx
import ast
import urllib.request
import zipfile
import matplotlib.pyplot as plt
import random
import numpy as np

edges = pd.read_csv('padgett/edges.csv')
nodes = pd.read_csv('padgett/nodes.csv')
G = nx.from_pandas_edgelist(edges, source='source', target='target', edge_attr=True)

mapping = {0:'ACCIAIUOL', 1:'ALBIZZI', 2:'BARBADORI', 3:'BISCHERI', 4:'CASTELLAN', 5:'GINORI', 6:'GUADAGNI', 7:'LAMBERTES', 8:'MEDICI', 9:'PAZZI', 10:'PERUZZI', 11:'PUCCI', 12:'RIDOLFI', 13:'SALVIATI', 14:'STROZZI', 15:'TORNABUON'}
G = nx.relabel_nodes(G, mapping)
G.add_node('PUCCI')
nx.draw(G, with_labels=True)

hc = nx.harmonic_centrality(G)
hc  = {key: value / 14 for key, value in hc.items()}
sorted(hc.items(), key=lambda x: x[1], reverse=True)

def initialize(degree_seq):
    return nx.havel_hakimi_graph(degree_seq)

def pick_double_swap(G):
    edges = list(G.edges())

    edge1, edge2 = random.sample(edges, 2)  

    if len(set(edge1) & set(edge2)) > 0:
        edge1, edge2 = random.sample(edges, 2)

    old_edges = [edge1, edge2]

    swap_edge1 = sorted((edge1[0], edge2[1]))
    swap_edge2 = sorted((edge1[1], edge2[0]))

    swap_edges = [(swap_edge1[0], swap_edge1[1]), (swap_edge2[0], swap_edge2[1])]
    return old_edges, swap_edges
    
def apply_swap(G, old_edges, swap_edges):
    if set(swap_edges).isdisjoint(G.edges()):
        G.remove_edges_from(old_edges)
        G.add_edges_from(swap_edges)

def MCMC(degree_seq):
    G = initialize(degree_seq)
    for _ in range(100):
        swap_edges, new_edges = pick_double_swap(G)
        apply_swap(G, swap_edges, new_edges)
    return G

degree_sequence = np.array([d for n, d in G.degree()])
mapping = {'ACCIAIUOL': 0, 'ALBIZZI': 1, 'BARBADORI': 2, 'BISCHERI': 3, 'CASTELLAN': 4, 'GINORI': 5, 'GUADAGNI': 6, 'LAMBERTES': 7, 'MEDICI': 8, 'PAZZI': 9, 'PERUZZI': 10, 'PUCCI': 11, 'RIDOLFI': 12, 'SALVIATI': 13, 'STROZZI': 14, 'TORNABUON': 15}
all_hcs = []
for i in range(1000):
    temp_G = MCMC(degree_sequence)
    hcs = nx.harmonic_centrality(temp_G, mapping)

    hcs  = {key: (value / 14) for key, value in hc.items()}

    all_hcs.append(hcs)
family_centrality_dists = {family:[] for family in mapping.values()}
for hc in all_hcs:
    for family, val in hc.items():
        family_centrality_dists[family].append(val)

fig, ax = plt.subplots()
ax.boxplot(family_centrality_dists.values())
ax.set_xticklabels(family_centrality_dists.keys())
plt.show()