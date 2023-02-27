import networkx as nx
import pandas as pd
import plotly.express as px

# For this analysis, I will choose computer science.

# edges from doctorate institution (node) u to faculty institution (node) v

# Load the edge data
edge_data = pd.read_csv('hiring_data//ComputerScience_edgelist.txt', sep='\t', header=None , names=['u', 'v', 'rank', 'gender'])

# Load the node data
node_data = pd.read_csv('hiring_data//ComputerScience_vertexlist.txt', sep='\t', header=None , names=['u', 'pi', 'USN2010', 'NRC95', 'Region', 'institution'])

# Create a directed graph
G = nx.from_pandas_edgelist(edge_data, 'u', 'v', create_using=nx.DiGraph())

# Add node metadata to the graph
for node, data in node_data.set_index('u').to_dict().items():
    nx.set_node_attributes(G, {node: data})

#plot US News ranking vs Eccentricity

# Get the strongly connected components
strong_components = nx.strongly_connected_components(G)

# Keep only nodes in the largest strongly connected component
largest_component = max(strong_components, key=len)
G = G.subgraph(largest_component)

# Compute eccentricity of each node
eccentricities = nx.eccentricity(G)

# Convert eccentricities to a DataFrame
ecc_df = pd.DataFrame.from_dict(eccentricities, orient='index', columns=['eccentricity'])
ecc_df.index.name = 'node'

# Merge the eccentricity data with the US News ranking data
result = pd.merge(ecc_df, node_data[['u', 'USN2010']], left_index=True, right_on='u')

# Plot the US News ranking by eccentricity
fig = px.scatter(result, x='USN2010', y='eccentricity')
fig.show()
