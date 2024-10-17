from classes import MachineUniverselle, RAMGraphBuilder
import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import json

def test_apuissanceb():
    """Tests the universal machine with the apuissanceb.ram program."""

    print("Test de la machine universelle avec le programme apowb.ram")
    mu = MachineUniverselle()
    rgb = RAMGraphBuilder()
    mu.load_input([rd.randint(0,10) for _ in range(2)])
    mu.build("apuissanceb.ram")
    mu.start()

def test_triabulle():
    """Tests the universal machine with the triabulle.ram program."""

    print("Test de la machine universelle avec le programme trieabulle.ram")
    mu = MachineUniverselle()
    rgb = RAMGraphBuilder()
    mu.load_input([rd.randint(0,10) for _ in range(10)])
    mu.build("triabulle.ram")
    mu.start()

def test_apuissanceb_with_graph():
    """Tests the universal machine with the apowb.ram program and visualizes the RAM graph.
    Deletes unreachable nodes and visualizes the updated RAM graph. Writes the graphs to JSON files and png files.
    Prints the number of nodes and edges in the graph before and after deleting unreachable nodes.
    Writes a new ram file without the deleted nodes and edges.
    Most of these methods comes from the RAMGraphBuilder class.
    """

    # Create MachineUniverselle instance
    mu = MachineUniverselle()
    mu.load_input([rd.randint(0, 10) for _ in range(2)])
    mu.build("apuissanceb.ram")
    mu.start()

    # Create RAM graph using RAMGraphBuilder
    code_path = "apuissanceb.ram"
    graph_builder = RAMGraphBuilder()
    ram_graph, nodes = graph_builder.create_ram_graph(code_path)

    # Visualize RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color = 'purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("apuissanceb_ram_graph.png")
    #plt.show()

# Save the graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("apuissanceb_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

    # Delete unreachable nodes
    graph_builder.delete_unreachable_nodes(ram_graph, code_path)

    # Visualize deleted RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color = 'purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("deleted_binarytodecimal_ram_graph.png")
    #plt.show()

    # Save the deleted graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("deleted_binarytodecimal_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

def test_triabulle_with_graph():
    """Tests the universal machine with the apowb.ram program and visualizes the RAM graph.
    Deletes unreachable nodes and visualizes the updated RAM graph. Writes the graphs to JSON files and png files.
    Prints the number of nodes and edges in the graph before and after deleting unreachable nodes.
    Writes a new ram file without the deleted nodes and edges.
    Most of these methods comes from the RAMGraphBuilder class.
    """

    # Create MachineUniverselle instance
    mu = MachineUniverselle()
    mu.load_input([rd.randint(0, 10) for _ in range(2)])
    mu.build("trieabulle.ram")
    mu.start()

    # Create RAM graph using RAMGraphBuilder
    code_path = "triabulle.ram"
    graph_builder = RAMGraphBuilder()
    ram_graph, nodes = graph_builder.create_ram_graph(code_path)

    # Visualize RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color = 'purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("triabulle_ram_graph.png")
    #plt.show()

# Save the graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("triabulle_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

    # Delete unreachable nodes
    graph_builder.delete_unreachable_nodes(ram_graph, code_path)

    # Visualize deleted RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color = 'purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("deleted_binarytodecimal_ram_graph.png")
    #plt.show()

    # Save the deleted graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("deleted_binarytodecimal_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

def test_binarytodecimal_with_graph():
    """Tests the universal machine with the binarytodecimal.ram program and visualizes the RAM graph.
    Deletes unreachable nodes and visualizes the updated RAM graph. Writes the graphs to JSON files and png files.
    Prints the number of nodes and edges in the graph before and after deleting unreachable nodes.
    Writes a new ram file without the deleted nodes and edges.
    Most of these methods comes from the RAMGraphBuilder class.
    """

    # Create MachineUniverselle instance
    mu = MachineUniverselle()
    mu.load_input([1010])
    mu.build("binarytodecimal.ram")
    mu.start()

    # Create RAM graph using RAMGraphBuilder
    code_path = "binarytodecimal.ram"
    graph_builder = RAMGraphBuilder()
    ram_graph, nodes = graph_builder.create_ram_graph(code_path)

    # Visualize RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color = 'purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("binarytodecimal_ram_graph.png")
    #plt.show()

    # Save the graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("binarytodecimal_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

    # Delete unreachable nodes
    graph_builder.delete_unreachable_nodes(ram_graph, code_path)

    # Visualize deleted RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color = 'purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("deleted_binarytodecimal_ram_graph.png")
    #plt.show()

    # Save the deleted graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("deleted_binarytodecimal_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

def test_toremovebinarytodecimal_with_graph():
    """Tests the universal machine with the toremovebinarytodecimal.ram program and visualizes the RAM graph.
    Deletes unreachable nodes and visualizes the updated RAM graph. Writes the graphs to JSON files and png files.
    Prints the number of nodes and edges in the graph before and after deleting unreachable nodes.
    Writes a new ram file without the deleted nodes and edges.
    Most of these methods comes from the RAMGraphBuilder class.
    The toremovebinarytodecimal.ram program is a modified version of the binarytodecimal.ram program with some unreachable nodes.
    So the new ram file will be the same as the binarytodecimal.ram program.
    """

    # Create MachineUniverselle instance
    mu = MachineUniverselle()
    mu.load_input([1010])
    mu.build("toremovebinarytodecimal.ram")
    mu.start()

    # Create RAM graph using RAMGraphBuilder
    code_path = "toremovebinarytodecimal.ram"
    graph_builder = RAMGraphBuilder()
    ram_graph, nodes = graph_builder.create_ram_graph(code_path)

    # Visualize RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color = 'purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("toremovebinarytodecimal_ram_graph.png")
    #plt.show()

    # Save the graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("toremovebinarytodecimal_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

    # Delete unreachable nodes
    graph_builder.delete_unreachable_nodes(ram_graph, code_path)

    # Visualize deleted RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color = 'purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("deleted_toremovebinarytodecimal_ram_graph.png")
    #plt.show()

    # Save the deleted graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("deleted_toremovebinarytodecimal_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

def test_combine_with_bonus():
    """Tests the universal machine with the bonus.ram program and visualizes the RAM graph.
    Writes the graphs to JSON files and png files.
    Combines consecutive instructions in the RAM file and writes a new ram file with the combined instructions.
    Most of these methods come from the RAMGraphBuilder class.
    """

    # Create MachineUniverselle instance
    mu = MachineUniverselle()
    mu.load_input([1010])
    mu.build("bonus.ram")
    mu.start()

    # Create RAM graph using RAMGraphBuilder
    code_path = "bonus2.ram" #"bonus.ram"
    graph_builder = RAMGraphBuilder()
    ram_graph, nodes = graph_builder.create_ram_graph(code_path)

    # Visualize deleted RAM graph
    plt.figure(figsize=(12, 8))
    nx.draw(ram_graph, with_labels=True, font_weight='bold', node_size=1, alpha=0.5, edge_color='purple')
    plt.title("Directed Graph of RAM Machine Instructions")
    plt.savefig("bonus_ram_graph.png")

    # Save the deleted graph to a JSON file
    data = nx.node_link_data(ram_graph)
    with open("bonus_ram_graph.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Number of nodes in the graph: ", len(ram_graph.nodes))
    print("Number of edges in the graph: ", len(ram_graph.edges))

    # Combine consecutive instructions in the RAM file
    graph_builder.combine_instructions(ram_graph, code_path)

if __name__ == "__main__":
    
    ###Questions 4 & 5
    #test_apuissanceb()
    #test_triabulle()

    ###Questions 8 & 9
    test_apuissanceb_with_graph()
    test_binarytodecimal_with_graph()
    test_toremovebinarytodecimal_with_graph()
    ###Question 10
    #test_combine_with_bonus()
    ###These are functions that test the universal machine with specific programs and visualize the RAM graph.
    ###But the RAMgraphBuilder could be used by simply one function that acts accordingly to the ram program given as argument.
    ###The code is wrote this way to show the different steps of the process and to test the different methods of the RAMGraphBuilder class in a clear way.
    ###Furthermore, it helps debugging and understanding the code and what is not currently working wiht machine universelle and RAMGraphBuilder.
    
    print("main.py : End.")