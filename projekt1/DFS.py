import numpy as np

class DFS():
    def __init__(self):
        self.graph = {}
        self.visited = set()

    def neighbourRow(self,arr, idx, idxS):
        arr_1 = arr[:idx][::-1]
        arr_2 = arr[idx + 1:]
        if len(arr_1) != 0 and arr_1[0] != -1:
            self.graph[(idxS, idx)].append((idxS, idx-1))

        if len(arr_2) != 0 and arr_2[0] != -1:
            self.graph[(idxS, idx)].append((idxS, idx+1))

    def neighbourCol(self,arr, idx, idxS):
        arr_1 = arr[:idx][::-1]
        arr_2 = arr[idx + 1:]
        if len(arr_1) != 0 and arr_1[0] != -1:
            self.graph[(idx, idxS)].append((idx - 1, idxS))

        if len(arr_2) != 0 and arr_2[0] != -1:
            self.graph[(idx, idxS)].append((idx + 1, idxS))

    def addNeighbour(self, x, idx, board_s):
        if x != -1:
            row = board_s[idx[0], :]
            column = board_s[:, idx[1]]
            self.graph[idx] = []
            self.neighbourRow(row, idx[1], idx[0])
            self.neighbourCol(column, idx[0], idx[1])

    def dfs(self, node):
        if node not in self.visited:
            self.visited.add(node)
            for neighbour in self.graph[node]:
                self.dfs(neighbour)

    def getNumberOfIslands(self, board_s, first):
        for idx, x in np.ndenumerate(board_s):
            self.addNeighbour(x, idx, board_s)

        islands = 0

        while len(self.graph) != len(self.visited):
            start = first
            stop = False

            for idx, x in np.ndenumerate(board_s):
                if idx not in self.visited and x != -1 and not stop:
                    start = idx
                    stop = True

            self.dfs(start)
            islands += 1

        return islands
