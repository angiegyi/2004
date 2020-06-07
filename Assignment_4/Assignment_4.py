from math import inf
import heapq
import copy

class Node:
    def __init__(self,value, ice_cream_type = False, ice = False, ice_state = False, ice_cream_state = False):
        self.value = value
        self.neighbours = []
        # self.states = states
        # self.state_nodes = []
        #
        #what kind of a node is it
        self.ice_cream = ice_cream_type
        self.ice = ice

        #what states the node are in
        self.ice_cream_state = ice_cream_state
        self.ice_state = ice_state


class Edge:
    def __init__(self,start_node,weight,end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight

class Graph:
    """
    Class representing a graph, uses an adjacency list representation
    """
    def __init__(self,gfile):
        self.nodes = []
        data = []
        file = open(gfile)

        for i in file:
            data.append(i.strip().split())

        self.number_of_nodes = int(data[0][0])
        self.table = [[inf for _ in range(self.number_of_nodes)] for _ in range(self.number_of_nodes)]

        #making the node list
        for i in range(self.number_of_nodes):
            self.nodes.append(Node(i))

        #adds neighbours to each node
        for i in range(1,len(data)):
            current_node = int(data[i][0])
            destination_node = int(data[i][1])
            self.nodes[current_node].neighbours += [Edge(current_node,int(data[i][2]), destination_node)]
            self.nodes[destination_node].neighbours += [(Edge(destination_node, int(data[i][2]), current_node))]


    def shallowest_spanning_tree(self):
        """
        Uses Floyd Warshall Algorithm to find the shallowest spanning tree
        Complexity: O(V^3) where V is the number of verticies in the graph
        :return: Tuple of the source vertex (int) and the shortest distance to the furthest node from the source (int)
        """

        if len(self.nodes) == 1:
            return 0, 0

        output = []

        #fill the adjacency table
        for node in self.nodes:
            for neighbour in node.neighbours:
                self.table[node.value][neighbour.end_node] = 1
                self.table[neighbour.end_node][node.value] = 1

        #O(V^3)
        for vertex_k in range(len(self.nodes)):
            for vertex_i in range(len(self.nodes)):
                for vertex_j in range(len(self.nodes)):
                    if vertex_i != vertex_j: #account for same node
                        self.table[vertex_i][vertex_j] = min(self.table[vertex_i][vertex_j], self.table[vertex_i][vertex_k] + self.table[vertex_k][vertex_j])

        #O(V^2)
        for row in self.table:
            temp = []
            for value in row:
                if value != inf:
                    temp.append(value)
            output.append((max(temp)))

        value = min(output)
        return (output.index(value),value)


    def shortest_errand(self, home, destination, ice_locs, ice_cream_locs):
        """
        Solve the problem of finding the shortest path from home to destination picking up ice and ice cream
        :param home: starting vertex
        :param destination: end vertex
        :param ice_locs: vertices where ice can be picked up
        :param ice_cream_locs: vertices where ice cream can be picked up
        :return: (length of the shortest path, path represented as a list of vertices)
        """

        #mark the old nodes for which one are ice and ice cream
        for node in ice_locs:
            self.nodes[node].ice = True

        for node in ice_cream_locs:
            self.nodes[node].ice_cream = True

        #copy the graph and reset node list
        copy_of_graph = [[] for _ in range(self.number_of_nodes)]

        #add the new verticies

        for node in self.nodes: #iterate through original node list and check type of node

            # indicates this is a plain node
            if node.ice is False and node.ice_cream is False:
                copy_of_graph[node.value].append(Node(node.value, False, False, True, True))  # Normal Node State - TT
                copy_of_graph[node.value].append(Node(node.value, False, False, False, False))  # Normal Node State - FF
                copy_of_graph[node.value].append(Node(node.value, False, False, True, False))  # Normal Node State - TF

            # node is ice and ice cream
            elif node.ice is True and node.ice_cream is True:
                copy_of_graph[node.value].append(Node(node.value, False, True, True, True))   # Ice Node State - TT
                copy_of_graph[node.value].append(Node(node.value, False, True, True, False))  # Ice Node State - TF
                copy_of_graph[node.value].append(Node(node.value, True, False, False, False)) # Ice Cream Node State - FF

            # node is just ice
            elif node.ice is True:
                copy_of_graph[node.value].append(Node((node.value), False, True, True, True))  # Ice Node State - TT
                copy_of_graph[node.value].append(Node((node.value), False, True, True, False))  # Ice Node State - TF

            # node is just ice cream
            else:
                copy_of_graph[node.value].append(Node((node.value), True, False, True, True))  # Ice Cream  Node State - TT
                copy_of_graph[node.value].append(Node((node.value), True, False, False, False)) # Ice Cream Node State - FF

        #adding the edges

        for row in copy_of_graph:
            for node in row: #go through each node
                matching_neighbour_list = self.nodes[int(node.value)].neighbours #get original neighbour list

                for neighbour in matching_neighbour_list: #goes through each neighbour
                    current_node = self.nodes[neighbour.start_node]
                    destination_node = self.nodes[neighbour.end_node]
                    weight_of_edge = neighbour.weight
                    current_state = (node.ice_state,node.ice_cream_state) #of state node

                    # going from plain node to ice cream node
                    if (current_node.ice == False and current_node.ice_cream == False) and destination_node.ice_cream == True:

                        for corresponding_node in copy_of_graph[destination_node.value]:
                            if current_state == (corresponding_node.ice_state,corresponding_node.ice_cream_state): #you can switch between the same states
                                node.neighbours.append(Edge(current_node, weight_of_edge, destination_node))
                                node.neighbours.append(Edge(destination_node, weight_of_edge, current_node))

                    #plain node to ice
                    if (current_node.ice == False and current_node.ice_cream == False) and destination_node.ice == True:
                        pass

                    #going from ice to ice cream
                    elif current_node.ice == True and destination_node.ice_cream == True:
                        pass

                    #ice cream node to ice node
                    elif destination_node.ice == True and current_node.ice_cream == True:
                        pass

                    #if any node to plain node
                    elif destination_node.ice == False and destination_node.ice_cream == False:
                        pass

                    # for corresponding_node in copy_of_graph.nodes[destination_node.value]:
                    #     if current_state == (corresponding_node.ice_state,corresponding_node.ice_cream_state): #you can switch between the same states
                    #         node.neighbours.append(Edge(current_node, weight_of_edge, destination_node))
                    #         node.neighbours.append(Edge(destination_node, weight_of_edge, current_node))
                    #








        # return copy_of_graph.dijkstra(home)

    def dijkstra(self, home):
        """
        dijkstra's shortest path algorithm
        :param home: starting vertex
        :return: distances of shortest path from a source vertex to every other vertex, pred array containing the
        predecessors of each vertex
        """

        queue = []
        heapq.heapify(queue)

        pred = [None for _ in range(self.number_of_nodes)]
        dist = [inf for _ in range(self.number_of_nodes)]
        dist[home] = 0

        #make the queue
        for node in self.nodes:
            heapq.heappush(queue,(dist[node.value],node.value))

        #dijkstra main loop
        while len(queue) != 0:
            index = (heapq.heappop(queue))[1]
            current_vertex = self.nodes[index]
            for neighbour in current_vertex.neighbours:
                neighbour_node = neighbour.end_node #neighbour
                neighbour_cost = neighbour.weight #distance
                if (neighbour_cost + dist[current_vertex.value]) < dist[neighbour_node]:
                    dist[neighbour_node] = neighbour_cost + dist[current_vertex.value]
                    pred[neighbour_node] = current_vertex.value
                    heapq.heappush(queue,(dist[neighbour_node],neighbour_node))
        return dist

g = Graph('given_graph2')
print(g.shortest_errand(0,8,[1,5,8],[4,6]))




