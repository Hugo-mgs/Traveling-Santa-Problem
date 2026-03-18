# Traveling Santa Problem - TS(anta)P
## (1) a specification of the work to be performed (definition of the problem to be solved)
The Traveling Santa Problem is an optimization problem published by Kaggle in 2012 that consists of a "variation" of the Traveling Salesman Problem, where Santa has to find the shortest path between a set of houses. The variation is that we have to find two disjoint paths and minimize the length of the longest one. If one path contains an edge from A to B the other cannot contain either an edge from A to B or from B to A.

The input file consists of a .csv files with 3 collumns (id, x and y). The id is a unique identifier for each node. The x and y represent the coordinates of the node.

## (2) related work with references to works found in a bibliographic search (articles, web pages, and/or source code)
### Non-optimal, probably not very correct amateur solution
https://blog.habrador.com/2012/12/the-traveling-santa-problem.html

### First Steps (published on kaggle)
https://www.kaggle.com/code/javiabellan/starting-kernel-plotting-nearest-neighbor/notebook

### 2nd place solution (explanation + code)
https://www.kaggle.com/competitions/traveling-santa-problem/writeups/wleite-source-code-of-the-prize-winners

### 1st place solution (code)
https://github.com/usamec/travelling-santa

## (3) formulation of the problem as an optimization problem (solution representation, neighborhood/mutation and crossover functions, hard constraints, evaluation functions)
The solution consists of a .csv file with two sequences of node ids that represent the two paths found. The score is the distance of the longest path.
The distance between two nodes is the distance between their coordinates.
The distance of a path can be calculated using the following function:
```py
def total_distance(df_path):
    dist = (np.sqrt((df_path.x - df_path.x.shift())**2 +
                    (df_path.y - df_path.y.shift())**2)).sum()
    return round(dist,2)
```
There are no strict paths. Every node can be travelled to and from any other node.
The nearest neighbour can be found using the following greedy function:
```py
def nearest_neighbour(df):
    ids = df.index.values[1:]
    xy = np.array([df.x.values, df.y.values]).T[1:]
    path = [0,]
    for _ in tqdm(range(len(df)-1)):
        last_x, last_y = df.x[path[-1]], df.y[path[-1]]
        dist = ((xy - np.array([last_x, last_y]))**2).sum(-1)
        nearest_index = dist.argmin()
        path.append(ids[nearest_index])
        ids = np.delete(ids, nearest_index, axis=0)
        xy  = np.delete(xy,  nearest_index, axis=0)
    path.append(0)
    return path
```


## (4) implementation already carried out (programming language, development environment, data structures, etc.).