import os
import pandas as pd
import spacy
import networkx as nx

# Set data file path and graph file path
data_dir = 'data'
data_filename = 'local_data.csv'
data_path = os.path.join(data_dir, data_filename)
graph_path = os.path.join(data_dir, 'local_data_graph.csv')

# Instantiate Spacy model
nlp = spacy.load('en_core_web_sm')

# Load or create empty graph
if os.path.exists(graph_path):
    G = nx.read_edgelist(graph_path, delimiter=',', data=(('name', str), ('entity_type', str)))
else:
    G = nx.Graph()

# Process all data files in directory
for filename in os.listdir(data_dir):
    if filename != data_filename:
        continue

    # Load data from file using context manager
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'r') as f:
        df = pd.read_csv(filepath)

        # Process each row in data file
        for index, row in df.iterrows():
            # Extract entity from name column
            entity = nlp(row['name'])[0]
            entity_type = 'ENTITY'
            G.add_node(entity.lemma_, name=row['name'], entity_type=entity_type)

            # Extract and process named entities from description column
            for ent in nlp(row['description']).ents:
                G.add_node(ent.lemma_, entity_type=ent.label_, description="")
                G.add_edge(ent.lemma_, entity.lemma_, name="", entity_type="")

            # Extract and process related entities from description column
            for w in row['description'].split(' '):
                if w.lower() in entity.lemma_:
                    continue
                related_ent = nlp(w)[0]
                G.add_node(related_ent.lemma_, description="")
                G.add_edge(related_ent.lemma_, entity.lemma_, name="", entity_type="")


# Save graph to file
nx.write_edgelist(G, graph_path, delimiter=',', data=['name', 'entity_type'])
# Print summary of graph properties
print(f'Number of nodes: {G.number_of_nodes()}')
print(f'Number of edges: {G.number_of_edges()}')