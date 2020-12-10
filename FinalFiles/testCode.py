import csv
import pandas as pd

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
    graph2 = Graph()
    heuristics_pdata = []
    heuristics_gdata = []

    with open('results/predictedHeuristics.csv') as csvfile1:

        reader_H = csv.DictReader(csvfile1)
        # f = open('resultLSTMPredicted.csv', 'wb')
        for row1 in reader_H:
            heuristics_pdata.append(float(row1['ActualCost']))

    with open('results/groundTruthHeuristics.csv') as csvfile2:

        reader_H = csv.DictReader(csvfile2)
        # f = open('resultLSTMPredicted.csv', 'wb')
        for row1 in reader_H:
            heuristics_gdata.append(float(row1['Heuristics']))


    indx = 0
    indx2 = 0
    preds=[]
    ground=[]
    with open('results/predictedCost.csv') as csvfile:
        reader1 = csv.DictReader(csvfile)
        # f = open('resultLSTMPredicted.csv', 'wb')
        # w = csv.writer(f)

        row_count1 = 0
        splitSize1 = 5


        for row in reader1:

            if row_count1 <= splitSize1:
                graph.connect(str(row['Point1']), str(row['Point2']), float(row['PredictedCost']))
                row_count1 = row_count1 + 1

                if row_count1 == 5:
                    heuristics= {}
                    heuristics['A'] = 0
                    heuristics['B'] = heuristics_pdata[indx + 1]
                    heuristics['C'] = heuristics_pdata[indx]

                    indx = indx + 2
                    print("The cost using predicted values is:")
                    path = astar_search(graph, heuristics, 'A', 'B')
                    # w.writer(path)
                    print(path)
                    string=""
                    for key in path:
                        string+=key[0]+","
                    preds.append(string[0:len(string)-1])
                    print()
            else:
                print()
                graph.connect(str(row['Point1']), str(row['Point2']), float(row['PredictedCost']))
                row_count1 = 1

    with open('results/groundTruthCost.csv') as csvfile:

        reader2 = csv.DictReader(csvfile)

        f1 = open('resultLSTMActual.csv', 'wb')
        w1 = csv.writer(f1)

        row_count2 = 0
        splitSize2 = 5

        for row in reader2:
            if row_count2 <= splitSize2:
                graph.connect(str(row['Point1']), str(row['Point2']), float(row['ActualCost']))
                row_count2 = row_count2 + 1
                if row_count2 == 5:
                    heuristics = {}
                    heuristics['A'] = 0
                    heuristics['B'] = heuristics_gdata[indx2 + 1]
                    heuristics['C'] = heuristics_gdata[indx2]
                    indx2+=2
                    print("The cost using Actual values is:")
                    path = astar_search(graph, heuristics, 'A', 'B')
                    # w1.writer(path)
                    print(path)
                    string = ""
                    for key in path:
                        string += key[0] + ","
                    ground.append(string[0:len(string) - 1])
                    print()
            else:
                print()
                graph.connect(str(row['Point1']), str(row['Point2']), float(row['ActualCost']))
                row_count2 = 1
    bools=[]
    for i in range(0,len(preds)):
        if(preds[i]==ground[i]):
            bools.append('yes')
        else:
            bools.append('no')
    data={'preds':preds,'ground':ground,'Yes/No':bools}
    df=pd.DataFrame(data=data,columns=['preds','ground','Yes/No'])
    df.to_csv('Results_LSTM.csv',index=False)
# Tell python to run main method
if __name__ == "__main__": main()
