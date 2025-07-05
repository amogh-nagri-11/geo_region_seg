import numpy as np
from scipy.spatial import distance_matrix

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i]) 
        return self.parent[i]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            self.parent[root_v] = root_u
            return True
        return False

def krushkal(location_df):
    coords = location_df[['x', 'y']].values
    dist_matrix = distance_matrix(coords, coords)

    n = len(coords)
    edges = [(dist_matrix[i][j], i, j) for i in range(n) for j in range(i + 1, n)]
    edges.sort() 

    ds = DisjointSet(n)
    mst = []

    for weight, u, v in edges:
        if ds.union(u, v):
            mst.append((u, v, weight))

    return mst

def build_graph_from_mst(mst, n):
    graph = {i: [] for i in range(n)}
    for u, v, weight in mst:
        graph[u].append((v, weight))
        graph[v].append((u, weight))
    return graph

def find_cost_between_hubs(graph, start, end):
    visited = set()
    def dfs(node, cost):
        if node == end:
            return cost
        visited.add(node)
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                result = dfs(neighbor, cost + weight)
                if result is not None:
                    return result
        return None
    return dfs(start, 0)
