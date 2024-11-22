import plotly.graph_objects as go
import networkx as nx

# Initialize the graph
G = nx.Graph()

# Define main nodes for Breast and Lung Cancer
main_nodes = ["Breast \n Cancer", "Lung \n Cancer"]

# Define genes and CpG sites for each cancer type
breast_genes = ["CDKL2", "BIRC8", "KCNG3", "THSD7A", "ASPA"]
breast_cpg_sites = ["#7737", "#10917", "#12986", "#86", "#3521"]

lung_genes = ["TP53", "EGFR", "ALK", "KRAS", "ROS1"]
lung_cpg_sites = ["#5623", "#9823", "#3409", "#2043", "#7854"]

# Add main nodes
for main_node in main_nodes:
    G.add_node(main_node)

# Add edges for Breast Cancer genes and CpG sites
for gene in breast_genes:
    G.add_edge(main_nodes[0], gene)
for cpg in breast_cpg_sites:
    G.add_node(cpg)

# Add edges for Lung Cancer genes and CpG sites
for gene in lung_genes:
    G.add_edge(main_nodes[1], gene)
for cpg in lung_cpg_sites:
    G.add_node(cpg)

# Position the nodes manually
pos = {
    main_nodes[0]: (-2, 0),  # Breast Cancer main node (left side)
    main_nodes[1]: (2, 0),   # Lung Cancer main node (right side)

    # Breast Cancer genes and CpG sites positions
    breast_genes[0]: (-4, 2),
    breast_genes[1]: (-4, 1),
    breast_genes[2]: (-4, 0),
    breast_genes[3]: (-4, -1),
    breast_genes[4]: (-4, -2),
    breast_cpg_sites[0]: (-6, 2),
    breast_cpg_sites[1]: (-6, 1),
    breast_cpg_sites[2]: (-6, 0),
    breast_cpg_sites[3]: (-6, -1),
    breast_cpg_sites[4]: (-6, -2),

    # Lung Cancer genes and CpG sites positions
    lung_genes[0]: (4, 2),
    lung_genes[1]: (4, 1),
    lung_genes[2]: (4, 0),
    lung_genes[3]: (4, -1),
    lung_genes[4]: (4, -2),
    lung_cpg_sites[0]: (6, 2),
    lung_cpg_sites[1]: (6, 1),
    lung_cpg_sites[2]: (6, 0),
    lung_cpg_sites[3]: (6, -1),
    lung_cpg_sites[4]: (6, -2)
}

# Define placeholder expression levels for genes (0 = low, 1 = high)
expression_levels = {
    # Breast Cancer genes
    breast_genes[0]: 0.1,
    breast_genes[1]: 0.4,
    breast_genes[2]: 0.7,
    breast_genes[3]: 0.9,
    breast_genes[4]: 0.3,

    # Lung Cancer genes
    lung_genes[0]: 0.2,
    lung_genes[1]: 0.5,
    lung_genes[2]: 0.8,
    lung_genes[3]: 0.6,
    lung_genes[4]: 0.4
}

# Define relative importance for CpG Sites with varied sizes for each cancer type
cpg_sizes = {
    # Breast Cancer CpG Sites
    breast_cpg_sites[0]: 20,
    breast_cpg_sites[1]: 30,
    breast_cpg_sites[2]: 40,
    breast_cpg_sites[3]: 25,
    breast_cpg_sites[4]: 15,

    # Lung Cancer CpG Sites with varied sizes
    lung_cpg_sites[0]: 18,
    lung_cpg_sites[1]: 26,
    lung_cpg_sites[2]: 32,
    lung_cpg_sites[3]: 29,
    lung_cpg_sites[4]: 22
}
default_gene_size = 30  # Default size for genes

# Specify connections between genes and CpG sites for dashed edges
dashed_edges = [
    # Breast Cancer gene-CpG relationships
    (breast_genes[0], breast_cpg_sites[4]),
    (breast_genes[1], breast_cpg_sites[3]),
    (breast_genes[2], breast_cpg_sites[2]),
    (breast_genes[3], breast_cpg_sites[1]),
    (breast_genes[4], breast_cpg_sites[3]),
    (breast_genes[4], breast_cpg_sites[0]),

    # Lung Cancer gene-CpG relationships
    (lung_genes[0], lung_cpg_sites[1]),
    (lung_genes[1], lung_cpg_sites[0]),
    (lung_genes[2], lung_cpg_sites[4]),
    (lung_genes[3], lung_cpg_sites[2]),
    (lung_genes[4], lung_cpg_sites[1]),
    (lung_genes[1], lung_cpg_sites[3])
]

# Extract positions for Plotly
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

# Dashed edges positions for gene-CpG relationships
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

# Draw dashed edges for gene-CpG relationships
dashed_trace = go.Scatter(
    x=dashed_x, y=dashed_y,
    line=dict(width=1, color='#888', dash='dash'),
    hoverinfo='none',
    mode='lines'
)

# Draw nodes with color and size distinctions
node_x = []
node_y = []
node_label_text = []
node_hover_info = []
node_sizes = []
node_shapes = []
node_colors = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_label_text.append(node)

    # Set hover information with line breaks
    if node in main_nodes:
        node_hover_info.append(f'{node} Origin Location<br>Severity Rank: INSERT')
        node_colors.append('blue')  # Uniform color for main nodes
        node_sizes.append(default_gene_size)
        node_shapes.append("circle")
    elif node in breast_genes or node in lung_genes:
        node_hover_info.append(f"{node}<br>Expression level: {expression_levels[node]:.1f}")
        node_colors.append(expression_levels[node])  # Color according to expression level
        node_sizes.append(default_gene_size)
        node_shapes.append("circle")
    else:  # CpG sites
        node_hover_info.append(f"{node}<br>Relative Importance (size): {cpg_sizes[node]}")
        node_colors.append('lightgray')  # Uniform color for CpG sites
        node_sizes.append(cpg_sizes[node])  # Varying sizes for importance
        node_shapes.append("triangle-up")

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_label_text,
    textposition="bottom center",
    hovertext=node_hover_info,
    hoverinfo='text',
    marker=dict(
        showscale=True,  # Show color scale for gene expression
        colorscale='RdBu',  # Red to Blue scale for genes
        cmin=0,  # Minimum expression value for scale
        cmax=1,  # Maximum expression value for scale
        color=node_colors,  # Uniform color for CpG, gradient for genes
        size=node_sizes,  # Size of CpG sites indicates importance
        symbol=node_shapes,  # Triangle for CpG, circle for others
        colorbar=dict(
            thickness=15,
            title='Expression Level (Genes)',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)
    )
)

# Add annotation to indicate CpG site importance key, positioned on the right side
fig = go.Figure(data=[edge_trace, dashed_trace, node_trace],
                layout=go.Layout(
                    title='Cancer Network with Expression Levels',
                    title_x=0.5,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[
                        dict(
                            x=0.5, y=1, xref='paper', yref='paper',
                            text='CpG Site Importance (Triangle Size)',
                            showarrow=False,
                            font=dict(size=12)
                        )
                    ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))

fig.show()
## In pop-up for cancer nodes, include information about where data came from (include ref link or self-report statement); include model information
## Can use "CpG" with varying font sizes to represent rather than triangles
#main_node.color == #FFBF00
#Describe what feature connection score is: represent relative strength of connections
# Important to include confidence score, based on: # patients (>30), model accuracy, etc.
### Internally, do threshold analysis: comparison between 1500 and 30, 50, etc. (levels): apply to same dataset (1 cancer subset)
##### Use confidence score NOT accuracy: acc could just randomly fluctuate/spike due to small size
### Make it very clear what users need to upload

## Dedicate specific folder to uploads: if folder has file, then start the script
#### Once run, send file to another working directory: reset folder every run

# Run-time troubleshooting:
# option 1: users give emails and after results collection done, send results via emails
# option 2: give them separate link, save link and it will be live in 30-35 min
### Make link available for certain number of days, don't want forever

# Small note on webapp, if want to do for yourself available on GitHub (only results; can include basic parameters)
## Give them limited "playground" in terms of customizing paramaterization: if want to fully test, go to GitHub

## Side idea: LLM for troubleshooting of confidence scores (future)

# Include package with back-end methylation data that is installed with the app (comes with initial installation)

# 1: web (servers), 2: download locally, 3: docker system (instantiate environment)
