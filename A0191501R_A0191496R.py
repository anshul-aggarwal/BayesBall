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
    for nd in graph:
        children_nd = graph[nd]
        if node in children_nd:
            parent_nodes.append(nd)
    return parent_nodes

def getNodes_Directions(graph, X): #Check logic validity
    nodes_directions = []
    #1 means up (from node to parent), 0 means down direction (from node to child node)
    for node in X:
        #Children
        if len(graph[node]) > 0:
            nodes_directions.append((node, 0))
        
        #Parents
        node_parents = parents(node, graph)
        if len(node_parents) > 0:
            nodes_directions.append((node, 1))

    return nodes_directions

def is_independent(graph, X, Y, Z):
    L_to_be_visited = deepcopy(Z)       #List L in Algorithm - Nodes to be visited
    Ancestors = []      #List A in Algorithm - Ancestors of Z

    #Phase 1
    while(True):
        if len(L_to_be_visited) == 0:
            break
        node = L_to_be_visited[0]   #Select some Y fom L (taking the first node)
        L_to_be_visited.remove(node)
        if node not in Ancestors:
            L_to_be_visited.extend(parents(node, graph))
        Ancestors.append(node)
        

    #Phase 2
    L_to_be_visited = getNodes_Directions(graph, X)       #List L in Algorithm - (node,direction) to be visited   
    Visited = []      #List V in Algorithm - (node,direction) marked as visited
    Reachable = []      #List R in Algorithm - nodes reachable via active trail

    while(True):
        selected_node_dir = L_to_be_visited[0]      #(Y,d)
        L_to_be_visited.remove(selected_node_dir)
        if selected_node_dir not in Visited:
            if selected_node_dir[0] not in Z:
                Reachable.append(selected_node_dir[0])
            Visited.append(selected_node_dir)

            if selected_node_dir[1] == 1 and selected_node_dir[0] not in Z:
                for z in parents(selected_node_dir[0], graph):
                    L_to_be_visited.append((z, 1))
                for z in graph[selected_node_dir[0]]:
                    L_to_be_visited.append((z, 0))
            elif selected_node_dir[1] == 0:
                if selected_node_dir[0] not in Z:
                    for z in graph[selected_node_dir[0]]:
                        L_to_be_visited.append((z, 0))
                if selected_node_dir[0] in Ancestors:
                    for z in parents(selected_node_dir[0], graph):
                        L_to_be_visited.append((z, 1))

        if len(L_to_be_visited) == 0:
            break

    #Final Check
    independence_X_Y = True

    if len(set(Reachable).intersection(set(Y))) > 0:
        independence_X_Y = False

    return independence_X_Y


if __name__ == '__main__':
    graph = create_graph()
    Qs = read_queries()
    for X, Y, Z in Qs:
        output = 1 if is_independent(graph, X, Y, Z) else 0
        print(output)
