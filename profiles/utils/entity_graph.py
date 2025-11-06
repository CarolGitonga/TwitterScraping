# profiles/utils/entity_graph.py
import os
import networkx as nx
from pyvis.network import Network
import spacy
from profiles.models import RawPost

# Load spaCy model once globally
nlp = spacy.load("en_core_web_sm")

def generate_entity_graph(username, platform="Twitter"):
    """
    Generate an interactive entity co-occurrence graph for a user's posts.
    Returns the path to an HTML file rendered via PyVis.
    """
    posts = RawPost.objects.filter(profile__username=username, profile__platform=platform)
    if not posts.exists():
        return None

    # Extract named entities from all posts
    G = nx.Graph()
    print(f"🧠 Extracting entities for {username}...")

    for post in posts:
        doc = nlp(post.content)
        entities = [ent.text for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE", "PRODUCT"}]
        hashtags = [word for word in post.content.split() if word.startswith("#")]
        all_entities = list(set(entities + hashtags))

        # Connect entities that co-occur in same post
        for i in range(len(all_entities)):
            for j in range(i + 1, len(all_entities)):
                e1, e2 = all_entities[i], all_entities[j]
                if G.has_edge(e1, e2):
                    G[e1][e2]["weight"] += 1
                else:
                    G.add_edge(e1, e2, weight=1)

    if len(G.nodes) == 0:
        print("⚠️ No named entities found.")
        return None

    
    # Create interactive PyVis network
    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="black")
    net.barnes_hut(gravity=-20000, central_gravity=0.3, spring_length=100)
    net.from_nx(G)

    # Customize node size by degree (importance)
    for node in net.nodes:
        degree = G.degree(node["id"])
        node["size"] = 15 + degree * 3
        node["color"] = "#007bff" if node["id"].startswith("#") else "#28a745"

    # ✅ FIX: use write_html instead of show()
    output_dir = os.path.join("media")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{username}_entity_graph.html")
    net.write_html(output_path, notebook=False, local=True)

    print(f"✅ Entity graph written to {output_path}")
    return output_path

