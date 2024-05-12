import time
from mpi4py import MPI
import networkx as nx
import heapq

def dijkstra(graph, source_node):
    return nx.single_source_dijkstra_path_length(graph, source_node)


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    initialTime = time.time()
    results = {}
    centrality_results = {}

    # Create a graph and add edges
    if rank == 0:
        graph = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int)
        priority_queue = [(i, node) for i, node in enumerate(graph.nodes())]
        nodes = list(graph.nodes())  # Get list of nodes
        priority_queue = [(i, node) for i, node in enumerate(nodes)]
    else:
        graph = None
        priority_queue = None

    # Broadcast the graph and queue to all processors
    graph = comm.bcast(graph, root=0)
    priority_queue = comm.bcast(priority_queue, root=0)

    # Step 2: While pq is not empty, keep popping nodes and sending them to the parallel processors
    while priority_queue:
        _, node = heapq.heappop(priority_queue)

        # Only process the node if its rank matches this processor's rank
        if node % size == rank:
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
            if result:
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
        with open(f"output{size}.txt", "w") as output_file:
            # Print top 5 nodes with highest centrality values
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





