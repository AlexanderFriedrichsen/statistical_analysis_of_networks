
partition = [0,0,0,1,1,1]

def objective_function(g, partition):
    n = g.number_of_nodes()
    L= 0
    for i,j in it.combination(range(n),1):
        L += g.has_edge(i,j) * (partition[i] == partition[j])
    
    for i,j,k in it.combinations(range(n),3):
        L += g.has_edge(i,j) * g.has_edge(i,k) * g.has_edge(k,j) * (partition[i] == partition[j] * partition[i]==partition[k])
    
    return L
# clusim package for clustering

objective_function(g, partition)