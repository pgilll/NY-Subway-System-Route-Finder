# Prabhleen Gill
# Graph Theory Spring 2024
# Code for presentation of NY Subway System

import sys
from graph import *
from plot import *

# stores functions for constructing graph within program
class Graph(object):
    # initialization
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    #adds the nodes to the graph and checks that they're bidirectional
    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    # returns nodes
    def get_nodes(self):
        return self.nodes

    # initializes edges with weights
    def get_outgoing_edges(self, node):
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    # returns the weight of an edge connecting two given nodes
    def value(self, node1, node2):
        return self.graph[node1][node2]


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    shortest_path = {}
    previous_nodes = {}

    # assign nodes with largest values (maxsize)
    # assign starting point with 0
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0

    # perform breadth first search on nodes and assign lowest weight to current min node (update after each search)
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # perform search on neighbors of a node
        # calculate total distance as you search (tentative_value)
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node

        # mark as visited when search ends
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path

# creates path based on search results
def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    path.append(start_node)

    print("\nWe found the following best path with a distance of {} miles.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))

# displays stations
def display_stations(nodes):
    print("\nHere is a list of stations:")

    for node in sorted(nodes):
        print(f"  - {node}")
    print()

# output messages
graph = Graph(nodes, init_graph)

print("Welcome to the NY Subway System Route Finder!")

inputs = input("\nDo you want to see the list of the stations (YES/NO): ")
if inputs.lower() == "yes":
    display_stations(nodes)

source = input("Enter a source station: ")
destination = input("Enter a destination station: ")

previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=source)

print_result(previous_nodes, shortest_path, start_node=source, target_node=destination)

display = input("\nDo you want to view the visualization of the graph (YES/NO) ? ")

if display.lower() == "yes":
    plot_graph(previous_nodes, start_node=source, target_node=destination)


while display.lower() not in ["yes", "no"]:
    print("Invalid Input. Please Try again.")
    display = input("\nDo you want to view the visualization of the graph (YES/NO) ? ")
    if display.lower() == "yes":
        plot_graph(previous_nodes)
    if display.lower() == "no":
        break
