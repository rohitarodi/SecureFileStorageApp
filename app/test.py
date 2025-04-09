import networkx as nx
import matplotlib.pyplot as plt

def create_mttsp_transition_diagram():
    G = nx.DiGraph()
    
    # ----------------------------
    # 1) Define Nodes (26 total)
    # ----------------------------
    # For clarity, store each node as a string exactly as you want it labeled.
    # The layers below match the "Diagram Structure" from the question.
    layer_0 = ["S"]
    layer_1 = ["(s1, s6)", "(s6, s1)"]
    layer_2 = ["(s4, s6)", "(s6, s4)", "(s1, s8)", "(s8, s1)"]
    layer_3 = ["(s3, s6)", "(s6, s3)", "(s4, s8)", "(s8, s4)", "(s1, s7)", "(s7, s1)"]
    layer_4 = ["(s2, s6)", "(s6, s2)", "(s3, s8)", "(s8, s3)", "(s4, s7)", "(s7, s4)"]
    layer_5 = ["(s2, s8)", "(s8, s2)", "(s3, s7)", "(s7, s3)"]
    layer_6 = ["(s2, s7)", "(s7, s2)"]
    layer_7 = ["F"]

    # Add them to the graph, and keep track of layers in a dictionary
    all_layers = [layer_0, layer_1, layer_2, layer_3, layer_4, layer_5, layer_6, layer_7]
    for layer_index, layer_nodes in enumerate(all_layers):
        for node in layer_nodes:
            G.add_node(node, layer=layer_index)

    # ----------------------------
    # 2) Define Edges (43 total)
    # ----------------------------
    # The edges are exactly as described in the question.

    edge_list = [
        ("S", "(s1, s6)"),
        ("S", "(s6, s1)"),
        
        ("(s1, s6)", "(s4, s6)"),
        ("(s1, s6)", "(s6, s4)"),
        
        ("(s6, s1)", "(s1, s8)"),
        ("(s6, s1)", "(s8, s1)"),
        
        ("(s4, s6)", "(s3, s6)"),
        ("(s4, s6)", "(s6, s3)"),
        
        ("(s6, s4)", "(s4, s8)"),
        ("(s6, s4)", "(s8, s4)"),
        
        ("(s1, s8)", "(s4, s8)"),
        ("(s1, s8)", "(s8, s4)"),
        
        ("(s8, s1)", "(s1, s7)"),
        ("(s8, s1)", "(s7, s1)"),
        
        ("(s3, s6)", "(s2, s6)"),
        ("(s3, s6)", "(s6, s2)"),
        
        ("(s6, s3)", "(s3, s8)"),
        ("(s6, s3)", "(s8, s3)"),
        
        ("(s4, s8)", "(s3, s8)"),
        ("(s4, s8)", "(s8, s3)"),
        
        ("(s8, s4)", "(s4, s7)"),
        ("(s8, s4)", "(s7, s4)"),
        
        ("(s1, s7)", "(s4, s7)"),
        ("(s1, s7)", "(s7, s4)"),
        
        ("(s7, s1)", "F"),
        
        ("(s2, s6)", "F"),
        
        ("(s6, s2)", "(s2, s8)"),
        ("(s6, s2)", "(s8, s2)"),
        
        ("(s3, s8)", "(s2, s8)"),
        ("(s3, s8)", "(s8, s2)"),
        
        ("(s8, s3)", "(s3, s7)"),
        ("(s8, s3)", "(s7, s3)"),
        
        ("(s4, s7)", "(s3, s7)"),
        ("(s4, s7)", "(s7, s3)"),
        
        ("(s7, s4)", "F"),
        
        ("(s2, s8)", "F"),
        
        ("(s8, s2)", "(s2, s7)"),
        ("(s8, s2)", "(s7, s2)"),
        
        ("(s3, s7)", "(s2, s7)"),
        ("(s3, s7)", "(s7, s2)"),
        
        ("(s7, s3)", "F"),
        
        ("(s2, s7)", "F"),
        ("(s7, s2)", "F")
    ]

    # Add edges to the graph
    for u, v in edge_list:
        G.add_edge(u, v)

    return G

def draw_mttsp_diagram(G, filename=None):
    """
    Draws the MTTSP transition diagram using a hierarchical layout (via Graphviz if available).
    If filename is provided, saves the diagram to that file (e.g., diagram.png).
    """
    # Attempt to use Graphviz layout if possible
    try:
        # Convert to a graphviz AGraph for hierarchical layout
        A = nx.nx_agraph.to_agraph(G)
        A.graph_attr["rankdir"] = "TB"  # top-to-bottom
        # Let dot or neato do an automatic layered layout
        A.layout(prog="dot")
        
        # Draw to a temporary file or provided filename
        if filename:
            A.draw(filename)
            print(f"Diagram saved as {filename}")
        else:
            # Draw to a temporary in-memory image and display inline
            A.draw("temp_diagram.png")  
            # Now show it in matplotlib
            img = plt.imread("temp_diagram.png")
            plt.figure(figsize=(10, 12))
            plt.imshow(img)
            plt.axis("off")
            plt.title("Transition Diagram for the One-Dimensional MTTSP with 8 Targets")
            plt.show()
            
    except ImportError:
        print("Graphviz layout not available. Using NetworkX spring_layout as fallback.")
        pos = nx.spring_layout(G, k=0.8, seed=42)
        
        plt.figure(figsize=(10, 12))
        nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="white", edgecolors="black")
        nx.draw_networkx_labels(G, pos, font_size=8)
        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="-|>")
        plt.axis("off")
        plt.title("Fallback Layout (Spring) for the One-Dimensional MTTSP with 8 Targets")
        plt.show()

# -----------------------------
# Main script usage
# -----------------------------
if __name__ == "__main__":
    # 1) Create the graph
    diagram_graph = create_mttsp_transition_diagram()
    
    # 2) Draw (and optionally save) the diagram
    # Provide a filename (e.g. 'diagram.png') to save, or leave None to show inline.
    draw_mttsp_diagram(diagram_graph, filename=None)
