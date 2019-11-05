class node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class edge:
    def __init__(self, start, end, cost):
        self.start = start
        self.end = end
        self.cost = cost


class sol:
    def __init__(self, nodes, edges, total_cost):
        self.nodes = nodes      #array of nodes in solution
        self.edges = edges      #array of edges in solution
        self.total_cost = total_cost