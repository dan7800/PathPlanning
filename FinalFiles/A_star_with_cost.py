class Graph:
    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    # Create an undirected graph by adding symmetric edges
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist

    # Add a link from A and B of given utility which is reward/cost,
    # and also add the inverse link if the graph is undirected
    def connect(self, A, B, cost=1):

        self.graph_dict.setdefault(A, {})[B] = cost
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = cost

    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name

    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f

    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))


# A* search
def astar_search(graph, heuristics, start, end):
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)

    # Loop until the open list is empty
    while len(open) > 0:
        # Sort the open list to get the node with the lowest cost first
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
        # Add the current node to the closed list
        closed.append(current_node)

        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ': ' + str(current_node.g))
                current_node = current_node.parent
            path.append(start_node.name + ': ' + str(start_node.g))
            # Return reversed path
            return path[::-1]
        # Get neighbours
        neighbors = graph.get(current_node.name)
        # Loop neighbors
        for key, value in neighbors.items():
            # Create a neighbor node
            neighbor = Node(key, current_node)
            # Check if the neighbor is in the closed list
            if (neighbor in closed):
                continue
            # Calculate full path cost
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if (add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)
    # Return None, no path is found
    return None


# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True



def main():
    # Create a graph
    graph = Graph()
    # Create graph connections (Actual cost)
    graph.connect('A', 'B', 10)
    graph.connect('A', 'C', 4)
    graph.connect('C', 'B', 1)
    graph.connect('B', 'C', 3)
    graph.connect('B', 'A', 5)
    graph.connect('C', 'A', 5)

    graph.make_undirected()

    heuristics = {}
    heuristics['A'] = 0
    heuristics['B'] = 10
    heuristics['C'] = 5

    graph2= Graph()
    # Create graph connections (Predicted cost)
    graph2.connect('A', 'B', 10)
    graph2.connect('A', 'C', 13)
    graph2.connect('C', 'B', 2)
    graph2.connect('B', 'C', 5)
    graph2.connect('B', 'A', 7)
    graph2.connect('C', 'A', 7)

    graph2.make_undirected()

    heuristics = {}
    heuristics['A'] = 0
    heuristics['B'] = 10
    heuristics['C'] = 5
    heuristics['E'] = 5
    heuristics['F'] = 3

    # Run the search algorithm
    print("The cost using predicted values is:" )
    path = astar_search(graph, heuristics, 'A', 'B')
    print(path)
    print()

    print("The cost using actual values is:")
    path = astar_search(graph2, heuristics, 'A', 'B')
    print(path)
    print()


# Tell python to run main method
if __name__ == "__main__": main()