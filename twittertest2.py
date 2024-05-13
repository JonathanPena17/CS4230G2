import time
from mpi4py import MPI
import networkx as nx
import numpy as np

def dijkstra(graph, source_node):
    return nx.single_source_dijkstra_path_length(graph, source_node)

def distribute_nodes(nodes, size):
    chunk_size = len(nodes) // size
    return [nodes[i:i + chunk_size] for i in range(0, len(nodes), chunk_size)]

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    initialTime = time.time()
    results = {}
    centrality_results = {}

    # Root process creates the graph and distributes nodes
    if rank == 0:
        graph = nx.read_edgelist("twitter_combined.txt", create_using=nx.Graph(), nodetype=int)
        nodes = list(graph.nodes())
        node_chunks = distribute_nodes(nodes, size)
    else:
        graph = None
        node_chunks = None

    # Scatter node chunks and broadcast graph
    node_chunk = comm.scatter(node_chunks, root=0)
    graph = comm.bcast(graph, root=0)

    # Process nodes in the received chunk
    for node in node_chunk:
        # Calculate Dijkstra's algorithm
        shortest_paths = dijkstra(graph, node)

        # Store the result
        results[node] = shortest_paths

        # Calculate and store the closeness centrality
        centrality = nx.closeness_centrality(graph, node)
        centrality_results[node] = centrality

    all_results = comm.gather(centrality_results, root=0)

    if rank == 0:
        # Ensure all results are ready before printing
        all_centrality_values = []
        for result in all_results:
            all_centrality_values.extend(result.items())

        # Get the top 5 nodes by maximum centrality values
        top_5 = sorted(all_centrality_values, key=lambda x: x[1], reverse=True)[:5]
        average_centrality = sum(centrality for _, centrality in all_centrality_values) / len(all_centrality_values)

        # Print top 5 nodes by maximum centrality values
        print("The top 5 nodes by maximum centrality values are:")
        for node, centrality in top_5:
            print(f"Node {node}: Closeness Centrality {centrality}")

        print(f"Runtime : {time.time() - initialTime}")
        print(f"Number of Processors: {size}\n")

        # Write results to file
        with open(f"outputTwitter{size}.txt", "w") as output_file:
            output_file.write("Top 5 Nodes by Maximum Centrality Values:\n")
            for node, centrality in top_5:
                output_file.write(f"Node {node}: Closeness Centrality {centrality}\n")
            output_file.write("\n\n")
            
            output_file.write(f"Average Centrality Value: {average_centrality}\n\n")
            
            output_file.write(f"Runtime : {time.time() - initialTime}\n\n")
            
            output_file.write(f"Number of Processors: {size}\n\n")
            
            output_file.write("Centrality Measures for All Vertices:\n")
            for node, centrality in sorted(centrality_results.items()):
                output_file.write(f"Node {node}: Closeness Centrality {centrality}\n")
            output_file.write("\n")
