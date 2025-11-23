import pandas as pd
from itertools import combinations
from collections import Counter
import networkx as nx
import plotly.graph_objects as go

def hashtags_association(df, top_n_pairs=30):
    # buat semua pasangan hashtag
    hashtag_pairs = [pair for sublist in df["hashtags"] for pair in combinations(sorted(set(sublist)), 2)]
    pair_counts = Counter(hashtag_pairs)
    df_pairs = pd.DataFrame(pair_counts.items(), columns=['pair','count']).sort_values(by='count', ascending=False)
    
    df_top = df_pairs.head(top_n_pairs)

    # buat graph network
    G = nx.Graph()
    for _, row in df_top.iterrows():
        G.add_edge(row['pair'][0], row['pair'][1], weight=row['count'])
    
    # posisi node
    pos = nx.spring_layout(G, k=0.5, seed=42)

    # buat edge traces
    edge_x = []
    edge_y = []
    weights = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        weights.append(edge[2]['weight'])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # buat node traces
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=20,
            color='skyblue'
        )
    )

    # gabungkan figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=None,
                        showlegend=False,
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='white'
                    ))
    
    return df_top.reset_index(), fig