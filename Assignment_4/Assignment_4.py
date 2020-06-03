from math import inf
import heapq

class Node:
    def __init__(self,value):
        self.value = value
        self.neighbours = []

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
        #queue is the distances linked with the node
        #shortest

        pass

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

g = Graph('fancy_graph')
print(g.shallowest_spanning_tree())










