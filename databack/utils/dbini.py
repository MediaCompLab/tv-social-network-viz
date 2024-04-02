import pandas as pd
import sys,os
import sqlite3
from sqlalchemy import create_engine

import networkx as nx
import numpy as np
import json

from config import host,username,password,port,db as DB,SQLALCHEMY_DATABASE_URI

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{DB}",echo=True)

print(os.path.abspath(os.getcwd()))
def calculate_graph_json(df):
    graphs = []
    step_info = []

    graph = nx.Graph()
    for idx, row in df.iterrows():
        if idx%1000 == 0:
            print(f'Processing row {idx}')
        # turn listener into list: "['Sheldon', 'Howard', 'Leonard', 'Raj']"
        # to list: ['Sheldon', 'Howard', 'Leonard', 'Raj']
        step_info.append((row['Season'], row['Episode'], row['Scene'], row['Line']))
        speaker = row['Speaker']
        listeners = []
        if isinstance(row["Listener"], str) and row['Listener'] != '[]':
            listeners = row['Listener'].split(',')
            # strip whitespace for each listener
            listeners = [listener.strip() for listener in listeners]
        # add speaker and listeners as nodes
        if speaker not in graph:
            graph.add_node(speaker, count=1)
        else:
            graph.nodes[speaker]['count'] += 1

        for listener in listeners:
            if listener not in graph:
                graph.add_node(listener, count=1)
            else:
                graph.nodes[listener]['count'] += 1
            if graph.has_edge(speaker, listener):
                graph[speaker][listener]['weight'] += 1
            else:
                graph.add_edge(speaker, listener, weight=1)

        graphs.append(graph.copy())

    pos = nx.spring_layout(graph)
    pos_scaled = nx.rescale_layout_dict(pos, scale=100)

    # Color scale for nodes and edges based on their count or weight
    node_count = [data['count'] for node, data in graph.nodes(data=True)]
    edge_weight = [data['weight'] for u, v, data in graph.edges(data=True)]
    min_max_node = (min(node_count), max(node_count))
    min_max_edge = (min(edge_weight), max(edge_weight))
    # add pos property to each node of all graphs
    i = 0
    for g in graphs:
        if i%1000 == 0:
            print(f'Processing graph {i}')
        for node in g.nodes:
            g.nodes[node]['x'] = pos_scaled [node][0]
            g.nodes[node]['y'] = pos_scaled [node][1]

        # add color scale for nodes and edges of all graphs
        for node in g.nodes:
            g.nodes[node]['color'] = np.interp(g.nodes[node]['count'], min_max_node, (0.1, 1))
        for u, v, data in g.edges(data=True):
            data['color'] = np.interp(data['weight'], min_max_edge, (0.1, 1))

        g_data = nx.node_link_data(graphs[i])
        data_json = json.dumps(g_data, indent=4)
        df.at[i, 'Result'] = data_json
        i += 1
    return df
def datainit(filename,batchno):
    print(f'---------------------- {filename} ----------------------')
    uploaddir = os.path.join(os.path.abspath(os.getcwd()), 'upload')
    file_path = os.path.join(uploaddir, filename)

    try:
        df = pd.read_csv(file_path)
        print("df:", df.shape)
        df['batchno'] = batchno
        df = calculate_graph_json(df)
        # print(">>>>>>>>> result example:", df.loc[2]['Result'])
        df.head(10)
        df.to_sql('big', engine, index=False, if_exists='append', chunksize=10000)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        print(f"Empty CSV file: {file_path}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")