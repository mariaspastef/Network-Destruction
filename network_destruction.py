from collections import deque
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("num_nodes", type=int, help="the number of nodes you wish to delete")
parser.add_argument("input_file", type=str, help="the file that contains the information of the graph")

parser.add_argument("-c", "--toFirst", action="store_true", help="use the first way")
parser.add_argument("-r", "--radius",type=int , help="use the second way")

args = parser.parse_args()

num_nodes = args.num_nodes
input_file = args.input_file
radius = args.radius

g = {}

with open(input_file) as graph_input:
    for line in graph_input:
        insiders = [int(x) for x in line.split()]
        if len(insiders) != 2:
            continue
        if insiders[0] not in g:
            g[insiders[0]] = []
        if insiders[1] not in g:
            g[insiders[1]] = []
        g[insiders[0]].append(insiders[1])
        g[insiders[1]].append(insiders[0])

def first(g, num_nodes):
    for j in range(1, num_nodes+1):
        max_count = 0
        max = 0
        for key,value in g.items():
            temp_count = len(value)
            if max_count < temp_count:
                max_count = temp_count
                max = key
            elif max_count == temp_count:
                if key < max:
                    max_count = temp_count
                    max = key
        g.pop(max)
        for v in g.values():
            if max in v:
                v.remove(max)
        print(max, max_count)

#finds the distance of all nodes from the specified node.
def bfs(graph, node):
    q = deque([node])
    count = {node: 0}
    while q:
        v = q.popleft()
        for n in graph[v]:
            if n not in count:
                q.append(n)
                count[n] = count[v] + 1
    return count

#finds for every key the total influence.
def influencefinder(graph, radius):
    influence = [0] * (len(g) +1)
    ki = [0] * (len(graph) +1)
    s = [0] * (len(graph) + 1)
    for i in graph:
        l2 = graph.get(i)
        ki[i] = len(l2) -1
        for key, value in bfs(graph,i).items():
            if value == radius:
               l = length(graph, key)
               s[i] = s[i] + l
        influence[i] = ki[i] * s[i]
    return influence

def length(graph, node):
    for key, value in graph.items(): 
        if node == key:
            b = len(value) - 1
    return b

def second(radius, num_nodes):
    for i in range(1, num_nodes+1):
        if i == 1:      
            list = influencefinder(g, radius)
        else:
            ki = [0] * (len(g) +1)
            s = [0] * (len(g) + 1)
            for i in g:    
                l2 = g.get(i)
                ki[i] = len(l2) -1      
                for key, value in bfs(g,i).items():
                    if value <= radius +1 and value == radius:
                        l = length(g, key)
                        s[i] = s[i] + l
                list[i] = ki[i] * s[i]           
        max_count = 0
        max = 0
        for j in range(1, len(list)): 
            temp_count = list[j]
            if max_count < temp_count:
                max_count = temp_count
                max = j
            elif max_count == temp_count:
                if j < max:
                    max_count = temp_count
                    max = j
        g[max] = []
        list[max] = []
        for v in g.values():
            if max in v:
                v.remove(max) 
        print(max, max_count) 

if args.toFirst:       
    first(g,num_nodes)
if args.radius: 
    second(args.radius,num_nodes)