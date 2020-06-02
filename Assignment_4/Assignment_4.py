from math import inf
import heapq

class Node:
    def __init__(self,value):
        self.value = value
        self.neighbours = []

class Edge:
    def __init__(self,predecessor,weight,successor):
        self.start_node = predecessor
        self.end_node = successor
        self.weight = weight

class Graph:
    def __init__(self,gfile):
        self.edges = []
        self.nodes = []

        data = []

        file = open(gfile)
        for i in file:
            data.append(i.strip().split())

        node_number = data[0][0]
        self.number_of_nodes = int(node_number)
        self.table = [[inf for _ in range(self.number_of_nodes)] for _ in range(self.number_of_nodes)]

        for i in range(int(node_number)):
            self.nodes.append(Node(i))

        for i in range(1,len(data)):
            self.edges.append(Edge(int(data[i][0]),int(data[i][2]),int(data[i][1])))

        for i in range(1,len(data)):
            current_node = int(data[i][0])
            destination_node = int(data[i][1])
            self.nodes[current_node].neighbours += [Edge(current_node,int(data[i][2]), destination_node)]
            self.nodes[destination_node].neighbours += [(Edge(destination_node, int(data[i][2]), current_node))]

        #make the table
        for edge in self.edges:
            self.table[edge.start_node][edge.end_node] = 1
            self.table[edge.end_node][edge.start_node] = 1

    def shallowest_spanning_tree(self):
        """
        Uses Floyd Warshall Algorithm to find the shallowest spanning tree
        Complexity: O(V^3) where V is the number of verticies in the graph
        :return: Tuple of the source vertex (int) and the shortest distance to the furthest node from the source (int)
        """

        output = []

        #O(V^3)
        for vertex_k in range(len(self.nodes)):
            for vertex_i in range(len(self.nodes)):
                for vertex_j in range(len(self.nodes)):
                    self.table[vertex_i][vertex_j] = min(self.table[vertex_i][vertex_j],self.table[vertex_i][vertex_k] + self.table[vertex_k][vertex_j])

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
        #queue is the distances linked with the node
        #shortest

        pass

    def dijstras(self,home):

        queue = []
        heapq.heapify(queue)

        pred = [None for _ in range(self.number_of_nodes)]
        dist = [inf for _ in range(self.number_of_nodes)]
        dist[home] = 0

        for node in self.nodes:
            heapq.heappush(queue,(dist[node.value],node.value))

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

g = Graph("test.txt")
print(g.dijstras(2))










