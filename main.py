import numpy as np
import pandas as pd
from core.graph import Graph, Edge, City

def main():
    in_file = pd.read_csv("input/random_50.csv")
    out_file = pd.read_csv("solution.csv")
    nearest_neighbour(in_file)

def total_distance(path):
    dist = (np.sqrt((path.x - path.x.shift())**2) +
            np.sqrt((path.y - path.y.shift())**2)
            ).sum()
    
    return round(dist, 2)

def nearest_neighbour(df):
    # gets all the node ids ignoring the first
    ids = df.index.values[1:]
    # gets and pairs all x and y values ignoring the first
    xy = np.array([df.x.values, df.y.values]).T[1:]
    path = [0,]
    for _ in range(len(df)-1):
        # gets x and y from last id in path
        last_x, last_y = df.x[path[-1]], df.y[path[-1]]
        # calculates the distance between every node and the last one
        dist = ((xy - np.array([last_x,last_y]))**2).sum(-1)
        # gets the nearest one
        nearest_idx = dist.argmin()
        path.append(ids[nearest_idx])
        # removes the found node from ids and xy
        ids = np.delete(ids, nearest_idx, axis=0)
        xy  = np.delete(xy,  nearest_idx, axis=0)
    # adds the origin to the end
    path.append(0)
    return path

if __name__ == "__main__":
    main()