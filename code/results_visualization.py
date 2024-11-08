import plotly.graph_objects as go
import networkx as nx
import numpy as np

# Initialize the graph
G = nx.Graph()

# Define main node, genes, and CpG sites
main_node = "Breast \n Cancer"
genes = ["CDKL2", "BIRC8", "KCNG3", "THSD7A", "ASPA"]
cpg_sites = ["#7737", "#10917", "#12986", "#86", "#3521"]

# Add nodes and edges for the main node and genes
G.add_node(main_node)
for gene in genes:
    G.add_edge(main_node, gene)

# Add edges between selected genes and CpG sites
G.add_edge(genes[0], cpg_sites[0])  # Connect CDKL2 with CPG Site #7737
G.add_edge(genes[1], cpg_sites[1])  # Connect BIRC8 with CPG Site #10917
G.add_edge(genes[2], cpg_sites[2])  # Connect KCNG3 with CPG Site #12986

# Additional dashed edges
dashed_edges = [(genes[0], cpg_sites[2]), (genes[1], cpg_sites[3]), (genes[2], cpg_sites[2]),
                (genes[3], cpg_sites[2]), (genes[1], cpg_sites[0]), (genes[2], cpg_sites[3]),
                (genes[4], cpg_sites[1]), (genes[4], cpg_sites[4])]

# Add nodes without default connections
for cpg in cpg_sites:
    G.add_node(cpg)

# Position the nodes manually
pos = {
    main_node: (0, 0),
    genes[0]: (2, 2),
    genes[1]: (2, 1),
    genes[2]: (2, 0),
    genes[3]: (2, -1),
    genes[4]: (2, -2),
    cpg_sites[0]: (4, 2),
    cpg_sites[1]: (4, 1),
    cpg_sites[2]: (4, 0),
    cpg_sites[3]: (4, -1),
    cpg_sites[4]: (4, -2),
}

# Define expression levels for each node (0 = low, 1 = high)
expression_levels = {
    main_node: 0.5,      # Breast Cancer (neutral)
    genes[0]: 0.1,       # Low expression for CDKL2
    genes[1]: 0.4,       # Moderate expression for BIRC8
    genes[2]: 0.7,       # Higher expression for KCNG3
    genes[3]: 0.9,       # Very high expression for THSD7A
    genes[4]: 0.3,       # Low-moderate expression for ASPA
    cpg_sites[0]: 0.2,   # CpG Site #7737 low
    cpg_sites[1]: 0.6,   # CpG Site #10917 moderate-high
    cpg_sites[2]: 0.8,   # CpG Site #12986 high
    cpg_sites[3]: 0.5,   # CpG Site #86 neutral
    cpg_sites[4]: 0.3    # CpG Site #3521 low-moderate
}

# Define relative importance for CpG Sites for node sizes
cpg_sizes = {
    cpg_sites[0]: 20,  # Size for CpG Site #7737
    cpg_sites[1]: 30,  # Size for CpG Site #10917
    cpg_sites[2]: 40,  # Size for CpG Site #12986
    cpg_sites[3]: 25,  # Size for CpG Site #86
    cpg_sites[4]: 15   # Size for CpG Site #3521
}
default_gene_size = 30  # Default size for genes and the main node

# Extract positions for Plotly
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

# Dashed edges positions
dashed_x = []
dashed_y = []
for edge in dashed_edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    dashed_x += [x0, x1, None]
    dashed_y += [y0, y1, None]

# Draw solid edges
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines'
)

# Draw dashed edges
dashed_trace = go.Scatter(
    x=dashed_x, y=dashed_y,
    line=dict(width=1, color='#888', dash='dash'),
    hoverinfo='none',
    mode='lines'
)

# Draw nodes with intensity-based colors and varying sizes for CpG sites
node_x = []
node_y = []
node_label_text = []
node_hover_info = []
node_sizes = []
node_shapes = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_label_text.append(node)

    # Set hover information with line breaks
    if node == 'Breast \n Cancer':
        node_hover_info.append('Cancer Origin Location: Breast<br>Severity Rank: 1')
    else:
        node_hover_info.append(f"{node}<br>Expression level: {expression_levels[node]:.1f}<br>Location: INSERT LOCATION")

    # Set size and shape: use CpG-specific sizes for CpG sites, default size for genes
    node_sizes.append(cpg_sizes[node] if node in cpg_sizes else default_gene_size)
    node_shapes.append("triangle-up" if node in cpg_sizes else "circle")

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_label_text,
    textposition="bottom center",
    hovertext=node_hover_info,
    hoverinfo='text',
    marker=dict(
        showscale=True,  # Show color scale
        colorscale='RdBu',  # Red to Blue scale
        cmin=0,  # Minimum expression value
        cmax=1,  # Maximum expression value
        color=list(expression_levels.values()),  # Use expression levels to color nodes
        size=node_sizes,  # Use varying sizes for CpG sites
        symbol=node_shapes,  # Set symbols based on node type
        colorbar=dict(
            thickness=15,
            title='Expression Level',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)
    )
)

# Create Plotly figure
fig = go.Figure(data=[edge_trace, dashed_trace, node_trace],
                layout=go.Layout(
                    title='Breast Cancer Network with Expression Levels',
                    title_x=0.5,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))

fig.show()


# IMPROVEMENT OF DIAGRAM:
# In case of no tissue correspondence (healthy or not), can standardize without control comparison
### Most data will have GTex
## Add pop-up upon click for more information about CpG Islands and Genes
## Vary CpG sites based on size rather than color (because do not use expression level but rather importance score)
## Can use triangles to represent CpG sites as well: helps users look at it as constant (easier size comparison)

# Use different icon for breast cancer: something to stand out --> https://bioart.niaid.nih.gov/bioart/60
# Include download button for diagram
# Consider genomic locations (Exact): build 37 or 38 (according to ...)
