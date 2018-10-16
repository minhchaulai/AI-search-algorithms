import numpy as np


def maze_to_graph(maze):
    ''' takes in a maze as a numpy array, converts to a graph '''
    # add your code here
    maze = maze.tolist()
    graph = {}
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            temp = {}
            if y + 1 < len(maze) and maze[y+1][x] == 0:
                temp[(x, y + 1)] = "N"
            if y - 1 > -1 and maze[y-1][x] == 0:
                temp[(x, y - 1)] = "S"
            if x -1 > -1 and maze[y][x-1] == 0:
                temp[(x - 1, y)] = "W"
            if x + 1 < len(maze[y]) and maze[y][x+1] == 0:
                temp[(x + 1, y)] = "E"
            graph[(x, y)] = temp
    # add your code here
    return graph
# Example 1 to print output
# testmaze = np.ones((4,4))
# testmaze[1,1] = 0
# testmaze[2,1] = 0
# testmaze[2,2] = 0
# testgraph = maze_to_graph(testmaze)
# print(testgraph[(1,1)])
# print(testgraph[(1,2)])
# print(testgraph[(2,2)])

# Example 2
# testmaze = np.array([[1, 1, 1, 1, 1],[1, 0, 0, 0, 1],[1, 0, 0, 0, 1],[1, 1, 1, 1, 1]])
# testgraph = maze_to_graph(testmaze)
# print(testgraph[(1,1)])
# print(testgraph[(1,2)])
# print(testgraph[(2,1)])
# print(testgraph[(2,2)])
# print(testgraph[(3,1)])
# print(testgraph[(3,2)])
