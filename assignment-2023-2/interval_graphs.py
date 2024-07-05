import argparse
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("task", help="The task that the user wants from the program to be executed")
parser.add_argument("file", help="The file with the graph")
args = parser.parse_args()
nodes = []
adjlist = dict()
with open(args.file, 'r') as file:
    lines = file.readlines()
for line in lines:
    n1, n2 = line.strip().split()
    n1, n2 = int(n1), int(n2)
    if n1 not in adjlist:
        adjlist[n1] = []
    if n2 not in adjlist:
        adjlist[n2] = []
    adjlist[n1].append(n2)
    adjlist[n2].append(n1)
for keys in adjlist:
    nodes.append(keys)
    adjlist[keys] = sorted(adjlist[keys])
nodes.sort()
nodes = [nodes]

def lexBFS(nodes, adjlist):
    nodes_copy = [[]]
    for i in nodes:
        for j in i:
            nodes_copy[0].append(j)
    lexorder = []
    while len(nodes_copy) > 0:
        x = nodes_copy[0].pop(0)
        if len(nodes_copy[0]) == 0:
            nodes_copy.pop(0)
        lexorder.append(x)
        neighbors = list(adjlist[x])
        pos = 0
        while len(neighbors) > 0:
            newSv = []
            for i in adjlist[x]:
                if i in lexorder:
                    if i in neighbors:
                        neighbors.remove(i)
                elif i in nodes_copy[pos]:
                    newSv.append(i)
                    nodes_copy[pos].remove(i)
                    neighbors.remove(i)
            if len(newSv) > 0:
                nodes_copy.insert(pos, newSv)
                pos = pos + 1
                if len(nodes_copy[pos]) == 0:
                    nodes_copy.pop(pos)
                    pos = pos - 1
            pos = pos + 1
    return lexorder

def chordal(reverse_lex_order, adjlist):
    j = 0 
    flag1 = True
    while j < len(reverse_lex_order) - 1 and flag1:
        u = reverse_lex_order[j]
        rn_u = set()
        flag2 = False
        i = j + 1
        pos = -1
        while not(flag2) and i < len(reverse_lex_order):
            if reverse_lex_order[i] in adjlist[u]:
                flag2 = True
                v = reverse_lex_order[i]
                pos = i
            else:
                i = i + 1
        if flag2 == True:
            rn_v = set()
            i = j + 1
            while i < len(reverse_lex_order):
                if reverse_lex_order[i] in adjlist[u]:
                    rn_u.add(reverse_lex_order[i])
                i = i + 1
            k = pos + 1
            while k < len(reverse_lex_order):    
                if reverse_lex_order[k] in adjlist[v]:
                    rn_v.add(reverse_lex_order[k])
                k = k + 1
            rn_u.remove(v)
        if rn_u.issubset(rn_v):
            j = j + 1
        else:
            flag1 = False
    if flag1 == True:
        return True
    else:
        return False

def bfs(nodes, adjlist, start_node):
    bfs_order = []
    queue = []
    visited = set()
    queue.append(start_node)
    visited.add(start_node)
    while len(queue) > 0:
        c = queue.pop(0)
        bfs_order.append(c)
        for v in adjlist[c]:
            if v not in visited and v not in queue:
                queue.append(v)
                visited.add(v)
    return bfs_order

def find_components(nodes, adjlist):
    c = [[] for _ in range(len(nodes[0]))]
    temp_dict = {}
    for i in nodes[0]:
        bfs_order = bfs(nodes, adjlist, i)
        bfs_order = [node for node in bfs_order if node not in adjlist[i] and node != i]
        for j in bfs_order:
            temp_set = set()
            temp_set.add(j)
            for k in bfs_order:
                if k in adjlist[j]:
                    temp_set.add(k)
            temp_dict[j] = temp_set
        keys = list(temp_dict.keys())
        keys_1 = 0
        keys_2 = 0
        for a in range(len(keys)):
            for b in range(keys_1 + 1, len(keys)):
                keys_1 = keys[a]
                keys_2 = keys[b]
                if keys_1 != keys_2:
                    if not temp_dict[keys_1].isdisjoint(temp_dict[keys_2]):
                        temp_dict[keys_1] = temp_dict[keys_1].union(temp_dict[keys_2])
                        temp_dict[keys_2] = temp_dict[keys_2].union(temp_dict[keys_1])
        for j in nodes[0]:
            if j in adjlist[i] or j == i:
                c[i].insert(j, 0)
            else:
                c[i].insert(j, temp_dict[j])
        temp_dict.clear()
    return c

def check_asteroidal_triples(nodes, adjlist):
    c = find_components(nodes, adjlist)
    for i in range(0,len(nodes[0])-2):
        for j in range(i+1,len(nodes[0])-1):
            for k in range(j+1, len(nodes[0])):
                if c[i][j] == c[i][k] and c[j][i] == c[j][k] and c[k][i] == c[k][j]:
                    if c[i][j] != 0 and c[i][k] !=0 and c[j][k] !=0:
                        return False
    return True

task = args.task
if task == "lexbfs":
    print(lexBFS(nodes, adjlist))
elif task == "chordal":
    lexorder = lexBFS(nodes, adjlist)
    lexorder.reverse()
    print(chordal(lexorder, adjlist))
elif task == "interval":
    lexorder = lexBFS(nodes, adjlist)
    lexorder.reverse()
    ischordal = chordal(lexorder, adjlist)
    if ischordal:
        at_free = check_asteroidal_triples(nodes, adjlist)
        if at_free:
            print(True)
        else:
            print(False)
    else:
        print(False)
