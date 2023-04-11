import numpy as np
import csv

def profile_likelihood(A, b):
    n = len(A)
    m = np.sum(A) / 2
    k = np.sum(A, axis=1)
    L = 0
    for r in set(b):
        nodes_r = [i for i in range(n) if b[i] == r]
        m_r = np.sum(A[nodes_r][:,nodes_r])
        k_r = np.sum(k[nodes_r])
        L += m_r * np.log(m_r / (k_r**2 / (2*m))) if m_r > 0 else 0
    L -= np.sum(k**2) / (4*m)
    return L

def initialize_assignment(n):
    return np.random.randint(2, size=n)

def compute_delta(A, b, i):
    n = len(A)
    m = np.sum(A) / 2
    k = np.sum(A, axis=1)
    nodes_i = np.where(b == b[i])[0]
    nodes_j = np.where(b != b[i])[0]
    m_ii = np.sum(A[nodes_i][:,nodes_i])
    m_ji = np.sum(A[nodes_j][:,nodes_i])
    k_i = np.sum(k[nodes_i])
    k_j = np.sum(k[nodes_j])
    delta = m_ji * np.log((m_ji + A[i,nodes_j].sum()) / (k_i * k_j / (2*m))) \
          + (m_ii - A[i,nodes_i].sum()) * np.log((m_ii - A[i,nodes_i].sum()) / (k_i**2 / (2*m)))
    return delta

def optimize_partition(A, b):
    n = len(A)
    m = np.sum(A) / 2
    k = np.sum(A, axis=1)
    L = profile_likelihood(A, b)
    while True:
        free_nodes = set(range(n))
        while free_nodes:
            deltas = [compute_delta(A, b, i) for i in free_nodes]
            i = free_nodes.pop(np.argmax(deltas))
            delta = deltas[i]
            L += delta
            b[i] = 1 - b[i]
            nodes_i = np.where(b == b[i])[0]
            nodes_j = np.where(b != b[i])[0]
            free_nodes.discard(i)
            for j in nodes_i:
                if j != i and j in free_nodes:
                    delta_j = compute_delta(A, b, j)
                    if delta_j < 0:
                        L += delta_j
                        b[j] = 1 - b[j]
                        free_nodes.add(i)
                        free_nodes.remove(j)
                        break
        if np.isclose(L, profile_likelihood(A, b)):
            break
    return b

def kernighan_lin(A):
    n = len(A)
    b = initialize_assignment(n)
    L = profile_likelihood(A, b)
    while True:
        b_best = b.copy()
        L_best = L
        for i in range(n):
            b[i] = 1 - b[i]
            b = optimize_partition(A, b)
            L = profile_likelihood(A, b)
            if L > L_best:
                b_best = b.copy()
                L_best = L
            b[i] = 1 - b[i]
        if np.array_equal(b, b_best):
            break
        b = b_best.copy()
        L = L_best
    return b



# Read in the edges from the CSV file
edges_file = "edges.csv"
edges = []
with open(edges_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    for row in reader:
        edges.append((int(row[0]), int(row[1])))

# Read in the nodes from the CSV file
nodes_file = "nodes.csv"
nodes = {}
with open(nodes_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    for row in reader:
        nodes[int(row[0])] = row[1]

# Construct the adjacency list using a dictionary
adj_list = {}
for edge in edges:
    if edge[0] not in adj_list:
        adj_list[edge[0]] = []
    if edge[1] not in adj_list:
        adj_list[edge[1]] = []
    adj_list[edge[0]].append(edge[1])
    adj_list[edge[1]].append(edge[0])


n_nodes = len(adj_list)
n_edges = sum(len(adj_list[node]) for node in adj_list)# // 2  # divide by 2 since edges are undirected
avg_degree = n_edges / n_nodes
max_degree = max(len(adj_list[node]) for node in adj_list)
min_degree = min(len(adj_list[node]) for node in adj_list)

print("Number of nodes:", n_nodes)
print("Number of edges:", n_edges)
print("Average degree:", avg_degree)
print("Maximum degree:", max_degree)
print("Minimum degree:", min_degree)

