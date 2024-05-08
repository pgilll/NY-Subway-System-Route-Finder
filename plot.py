import networkx as nx
import plotly.graph_objects as go
from graph import *

def plot_graph(previous_nodes, start_node, target_node):
    global connections, nodes
    G = nx.Graph()

    for source, target, weight in connections:
        G.add_edge(source, target, weight=weight)

    pos = nx.spring_layout(G, k=0.5, iterations=150)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = []
    node_y = []
    text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.8, color='black'), mode='lines')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=text, textposition='top center',
                            marker=dict(showscale=False, color='black', size=5), hoverinfo='text')

    path = []
    node = target_node
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
    path.append(start_node)
    path.reverse()

    shortest_edge_x = [pos[node][0] for node in path]
    shortest_edge_y = [pos[node][1] for node in path]

    shortest_path_trace = go.Scatter(x=shortest_edge_x, y=shortest_edge_y, line=dict(width=2.5, color='red'), mode='lines')

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Network graph of NY Subway System',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Python code with NetworkX and Plotly",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    fig.add_trace(shortest_path_trace)
    fig.update_layout(showlegend=False)

    fig.show()
