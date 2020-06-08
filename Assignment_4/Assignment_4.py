from math import inf
import heapq


class Node:
    """
    Class representing a node
    """
    def __init__(self,value, ice_cream_type = False, ice = False):
        self.value = value
        self.neighbours = []
        self.ice_cream = ice_cream_type
        self.ice = ice


class Edge:
    """
    Class representing an Edge which connects two vertices
    """
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
        return output.index(value),value

    def shortest_errand(self, home, destination, ice_locs, ice_cream_locs):
        """
        Solve the problem of finding the shortest path from home to destination picking up ice and ice cream
        :param home: starting vertex
        :param destination: end vertex
        :param ice_locs: vertices where ice can be picked up
        :param ice_cream_locs: vertices where ice cream can be picked up
        :return: (length of the shortest path, path represented as a list of vertices)
        Complexity: O(E log V) where E is the number of edges in the graph and V is the number of vertices in the graph
        """

        #first make a new graph
        copy_of_graph = self.construct_new_graph(ice_locs,ice_cream_locs)

        #run dijkstra's to get the shortest path from home -> destination
        answer = self.dijkstra(copy_of_graph,home)

        #store the dist and pred arrays
        dist,pred = answer[0],answer[1]

        #reconstruct the path
        return self.path_reconstruction(dist,pred,destination)

    def path_reconstruction(self,dist, pred, destination):
        """
        Rebuilds the path from dijkstra's using the existing pred array
        :param dist: distance array containing integers representing the length of a path from a source node to every
        other node
        :param pred: pred array containing integers representing the predecessor of a node at a given index
        :param destination: the destination node
        :return: a tuple of the length of getting from home to destination, and the path taken
        Complexity: O(P): where p is the length of the pred array
        """
        # rebuild path
        final_path = []
        u = (destination * 3) + 2
        final_path.append(u)

        while u != -1:
            u = pred[u]
            final_path.append(u)

        final_path.pop()
        final_path.reverse()

        # get original vertices back
        for i in range(len(final_path)):
            final_path[i] = final_path[i] // 3

        # remove duplicates
        i = 1
        while i != len(final_path):
            if final_path[i] == final_path[i - 1]:
                final_path.pop(i - 1)
                i -= 1
            i += 1

        return dist[u], final_path

    def construct_new_graph(self, ice_locs, ice_cream_locs):
        """
        Constructing the new graph
        :param ice_locs: list of integers indicating where the ice nodes are
        :param ice_cream_locs: list of integers indicating where the ice cream nodes are
        :return: a new graph of nodes and edges
        Complexity O(VE): where V is the number of vertices in the original graph and E is the number of edges in the
        original graph.
        """

        # mark the old nodes for which one are ice and ice cream
        for node in ice_locs:
            self.nodes[node].ice = True

        for node in ice_cream_locs:
            self.nodes[node].ice_cream = True

        # copy the graph and reset node list
        copy_of_graph = [Node(i) for i in range(self.number_of_nodes * 3)]

        # making 0 edges to connect each ice node and ice cream node through each layer
        for node_number in range(self.number_of_nodes):
            new_index = 3 * node_number
            if self.nodes[node_number].ice:
                copy_of_graph[new_index].neighbours.append(Edge(node_number, 0, new_index + 1))  # level 0 -> 1
            if self.nodes[node_number].ice_cream:
                copy_of_graph[new_index + 1].neighbours.append(
                    Edge(node_number + 1, 0, new_index + 2))  # level 1 -> level 2

        # making edges
        for node in self.nodes:
            original_vertex = 3 * node.value
            for neighbour_edge in node.neighbours:
                destination_node = neighbour_edge.end_node * 3
                weight = neighbour_edge.weight

                # making first level edges
                copy_of_graph[original_vertex].neighbours.append(Edge(original_vertex, weight, destination_node))
                copy_of_graph[destination_node].neighbours.append(Edge(destination_node, weight, original_vertex))

                # making second layer edges
                copy_of_graph[original_vertex + 1].neighbours.append(
                    Edge(original_vertex + 1, weight, destination_node + 1))
                copy_of_graph[destination_node + 1].neighbours.append(
                    Edge(destination_node + 1, weight, original_vertex + 1))

                # making final layer edges
                copy_of_graph[original_vertex + 2].neighbours.append(
                    Edge(original_vertex + 2, weight, destination_node + 2))
                copy_of_graph[destination_node + 2].neighbours.append(
                    Edge(destination_node + 2, weight, original_vertex + 2))

        return copy_of_graph

    def dijkstra(self, copy_of_graph, home):
        """
        dijkstra's shortest path algorithm
        :param copy_of_graph: graph which dijkstra will be performed on
        :param home: starting vertex
        :return: distances of shortest path from a source vertex to every other vertex, pred array containing the
        predecessors of each vertex
        Complexity: O(E Log V) where E is the number of edges in the graph and V is the number of vertices in the graph
        """
        queue = []
        heapq.heapify(queue)

        pred = [-1 for _ in range(self.number_of_nodes * 3)]
        dist = [inf for _ in range(self.number_of_nodes * 3)]
        dist[home * 3] = 0

        # make the queue
        for node in copy_of_graph:
            heapq.heappush(queue, (dist[node.value], node.value))

        # dijkstra main loop
        while len(queue) != 0:
            index = (heapq.heappop(queue))[1]
            current_vertex = copy_of_graph[index]
            for neighbour in current_vertex.neighbours:
                neighbour_node = neighbour.end_node  # neighbour
                neighbour_cost = neighbour.weight  # distance
                if (neighbour_cost + dist[current_vertex.value]) < dist[neighbour_node]:
                    dist[neighbour_node] = neighbour_cost + dist[current_vertex.value]
                    pred[neighbour_node] = current_vertex.value
                    heapq.heappush(queue, (dist[neighbour_node], neighbour_node))

        return dist, pred

g = Graph('fancy_graph')
print(g.shortest_errand(3,6,[5,4],[3,4]))




