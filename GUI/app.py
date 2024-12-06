from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
import time
import plotly.graph_objects as go
import networkx as nx

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Dummy username and password
USERNAME = "user"
PASSWORD = "pass"

@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/how_to_use')
def how_to_use():
    return render_template('how_to_use.html')

@app.route('/how_works')
def how_works():
    return render_template('how_works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Simulate a pipeline process
        run_pipeline(filepath)

        return redirect(url_for('results'))
    else:
        flash('Invalid file type. Please upload a CSV or TXT file.')
        return redirect(url_for('index'))

@app.route('/results')
@app.route('/results')
def results():
    # Create the Plotly figure
    fig = generate_cancer_network_plot()

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Pass the plot HTML to the template
    return render_template('results.html', plot=plot_html)


def generate_cancer_network_plot():
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
        main_nodes[0]: (-2, 0),
        main_nodes[1]: (2, 0),
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

    # Extract positions for Plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    # Draw solid edges
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Draw nodes with color and size distinctions
    node_x = []
    node_y = []
    node_label_text = []
    node_hover_info = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_label_text.append(node)
        node_hover_info.append(node)  # Add any additional information here

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_label_text,
        hovertext=node_hover_info,
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Importance',
                xanchor='left',
                titleside='right'
            )
        )
    )

    # Combine everything into a figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Cancer Network Visualization',
                        title_x=0.5,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    return fig


if __name__ == "__main__":
    app.run(debug=True)
