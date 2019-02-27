'''
Description: CS5340 - The Bayes-Ball algorithm
Name: Anshul Aggarwal, Amit Sukhpal
Matric No.: A0191501R, A0191496R
'''

from copy import deepcopy


def create_graph():
    """Reads graph.txt and returns a dictionary
    with nodes as keys and the value is a list of
    nodes that the given node has a directed edge to.

    Returns:
        dict: the graph as a dictionary
    """
    with open('graph.txt', 'r') as g_file:
        K = int(g_file.readline())
        graph = {i: [] for i in range(1, K + 1)}
        for line in g_file:
            i, j = map(int, line.split())
            graph[i].append(j)
    return graph


def read_queries():
    """Reads queries.txt and returns a list of X, Y, Z
    triplets.

    Returns:
        list: the list of queries
    """
    with open('queries.txt', 'r') as q_file:
        queries = []
        for line in q_file:
            X, Y, Z = [], [], []
            x, y, z = line.split()
            X.extend(map(int, filter(bool, x[1:-1].split(','))))
            Y.extend(map(int, filter(bool, y[1:-1].split(','))))
            Z.extend(map(int, filter(bool, z[1:-1].split(','))))
            queries.append([X, Y, Z])
    return queries

########################### NOTES ###############################
# Checks if X is conditionally indepedent
# of Y given Z.

# Args:
#     graph (dict): the Bayesian network
#     X (list): list of nodes in set X
#     Y (list): list of nodes in set Y
#     Z (list): list of nodes in set Z

# Returns:
#     bool: True if X is conditionally indepedent
# of Y given Z, False otherwise.

# graph is the Bayesian Network
# X is source variable
# Z is Observations

#################################################################

def parents(node, graph):
    parent_nodes = []
    for (nd, children_nd) in graph:
        if node in children_nd:
            parent_nodes.append(nd)
    return parent_nodes

def is_independent(graph, X, Y, Z):
    L_to_be_visited = deepcopy(Z)
    A_ancestors = []

    #Phase 1
    while(True):
        if len(L_to_be_visited) == 0:
            break
        node = L_to_be_visited[0]   #Select some Y fom L (taking the first node)
        L_to_be_visited.remove(node)
        if node not in A_ancestors:
            L_to_be_visited.extend(parents(node, graph))
            print(L)
        A_ancestors.append(node)
        

    #Phase 2
    L_to_be_visited = [(X, 1)]    #1 means up, 0 means down direction
    Visited = []
    Reachable = []

    #TODO

    #Final Check
    independence_X_Y = True

    if len(set(Reachable).intersection(set(Y))) > 0:
        independence_X_Y = False

    return independence_X_Y


if __name__ == '__main__':
    graph = create_graph()
    print(graph)
    Qs = read_queries()
    for X, Y, Z in Qs:
        output = 1 if is_independent(graph, X, Y, Z) else 0
        print(output)
