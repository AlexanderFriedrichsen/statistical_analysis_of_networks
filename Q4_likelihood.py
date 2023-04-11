import csv
import numpy as np

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

# Read in the edges from the CSV file
edges_file = "edges.csv"
edges = []
with open(edges_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    for row in reader:
        edges.append((int(row[0]), int(row[1])))

# Construct the adjacency list using a dictionary
adj_list = {}
for edge in edges:
    if edge[0] not in adj_list:
        adj_list[edge[0]] = []
    if edge[1] not in adj_list:
        adj_list[edge[1]] = []
    adj_list[edge[0]].append(edge[1])
    adj_list[edge[1]].append(edge[0])

# Initialize the community assignment vector
n_nodes = len(adj_list)
b = np.random.randint(2, size=n_nodes)

# Compute the profile log-likelihood
L = profile_likelihood(adj_list, b)
print("Profile log-likelihood:", L)
