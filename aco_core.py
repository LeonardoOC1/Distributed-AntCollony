# aco_core.py

import math
import random

class Edge:
    def __init__(self, a, b, weight, initial_pheromone):
        self.a = a
        self.b = b
        self.weight = weight
        self.pheromone = initial_pheromone

class Ant:
    def __init__(self, alpha, beta, num_nodes, edges):
        self.alpha = alpha
        self.beta = beta
        self.num_nodes = num_nodes
        self.edges = edges
        self.tour = []
        self.distance = 0.0

    def _select_node(self):
        current = self.tour[-1]
        unvisited = [i for i in range(self.num_nodes) if i not in self.tour]
        total = 0.0
        probs = []
        for node in unvisited:
            pheromone = self.edges[current][node].pheromone ** self.alpha
            heuristic = (1.0 / self.edges[current][node].weight) ** self.beta
            total += pheromone * heuristic
            probs.append((node, pheromone * heuristic))
        r = random.uniform(0, total)
        acc = 0.0
        for node, prob in probs:
            acc += prob
            if acc >= r:
                return node
        return unvisited[-1]

    def find_tour(self):
        self.tour = [random.randint(0, self.num_nodes - 1)]
        while len(self.tour) < self.num_nodes:
            self.tour.append(self._select_node())
        self.distance = sum(
            self.edges[self.tour[i]][self.tour[(i + 1) % self.num_nodes]].weight
            for i in range(self.num_nodes)
        )
        return self.tour, self.distance

def build_graph(nodes, initial_pheromone):
    num_nodes = len(nodes)
    edges = [[None] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            dist = math.dist(nodes[i], nodes[j])
            edges[i][j] = edges[j][i] = Edge(i, j, dist, initial_pheromone)
    return edges

def deposit_pheromone(edges, tour, distance, rho, Q=1.0):
    pheromone_to_add = Q / distance
    for i in range(len(tour)):
        a = tour[i]
        b = tour[(i + 1) % len(tour)]
        edges[a][b].pheromone = (1 - rho) * edges[a][b].pheromone + pheromone_to_add
        edges[b][a].pheromone = edges[a][b].pheromone

def clone_edges(edges):
    num_nodes = len(edges)
    new_edges = [[None] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(num_nodes):
            if edges[i][j] is not None:
                e = edges[i][j]
                new_edges[i][j] = Edge(e.a, e.b, e.weight, e.pheromone)
    return new_edges
