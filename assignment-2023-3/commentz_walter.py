import argparse
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("-v", action="store_true", help="Print the contents of s1 and s2 for each node")
parser.add_argument("search_terms", nargs="*", help="The patterns that we must search for in the text")
parser.add_argument("file", type = argparse.FileType("r"), help="The file with the text")
args = parser.parse_args()
text = args.file.read()
patterns = []
reversed_patterns = []
pmin = 1000
pmax = -1
for arg in args.search_terms:
    if len(arg) < pmin:
        pmin = len(arg)
    if len(arg) > pmax:
         pmax = len(arg)
    patterns.append(arg)
    reversed_patterns.append("".join(reversed(arg)))
ordinal = {
  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
  'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
  'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
  'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, ' ': 26
}

rt = []
def rtoccurences(ordinal):
    m = pmin + 1
    for i in range(0,26):
        rt.append(m)
    for p in patterns:
        m = len(p)
        for i in range(0,m):
            if m-i < rt[ordinal[p[i]]]:
                rt[ordinal[p[i]]] = m-i
    return rt

rt = rtoccurences(ordinal)

trie = {} #keys will be tuples with the nodes that are connected and values the weights-letter of the edge
end_of_word = {} #the value indicates whether the node that is represented by the key is the end of a word or not
trie_adj_list = {}
node_counter = 0 #we begin from the root of the trie
trie_adj_list[node_counter] = []
end_of_word[node_counter] = False
ending_nodes = []
for word in reversed_patterns: #we will insert in the trie every reversed pattern 
    "we will examine every letter of the word as we start from the root"
    root = 0
    letter_counter = 0
    "as long as the current letter matches one of the weights at the current depth we follow this path"
    "in the first mismatch we create a new branch"
    "the rest of the word is inserted in this new path"
    mismatch = False
    for letter in word:
        letter_counter += 1
        #we have already found a mismatch in the current word so we add the letters left at the new branch
        if mismatch:
            root = node_counter #new root is the one that we inserted with the previous letter
            if root not in trie_adj_list.keys(): #if the new root does not have children we insert it at the adjacency list 
                    trie_adj_list[root] = []
            node_counter += 1 
            end_of_word[node_counter] =  False
            trie[(root, node_counter)] = letter
            trie_adj_list[root].append(node_counter)
        else:
            #as we have not find a mismatch yet we examine all the children of the current root 
            if root in trie_adj_list.keys() and len(trie_adj_list[root]) > 0:
                flag = False
                for i in trie_adj_list[root]:
                    if trie[(root, i)] == letter: #if we found a match we update the root and move on the trie
                        root = i
                        flag = True
                        break
                if flag == False: #in this case we have found a mismatch. We create a new branch at the current root 
                    mismatch = True
                    node_counter += 1
                    end_of_word[node_counter] = False
                    trie[(root, node_counter)] = letter
                    trie_adj_list[root].append(node_counter)
                else:
                    root = i
            else:
                mismatch = True
                if root not in trie_adj_list.keys():
                    trie_adj_list[root] = []
                node_counter += 1
                end_of_word[node_counter] = False
                trie[(root, node_counter)] = letter
                trie_adj_list[root].append(node_counter)
    if len(word) == letter_counter:
        ending_nodes.append(node_counter)
for node in ending_nodes:
    end_of_word[node] = True
    if node not in trie_adj_list.keys():
        trie_adj_list[node] = []

depth = {}
depth[0] = 0
bfs_order = []
queue = []
visited = set()
queue.append((0, 0))
visited.add(0)
while len(queue) > 0:
    c, current_depth = queue.pop(0)
    bfs_order.append(c)
    for v in trie_adj_list[c]:
        if v not in visited and v not in queue:
            queue.append((v, current_depth + 1))
            visited.add(v)
            depth[v] = current_depth + 1
failure = {}
failure[0] = 0
for neighbor in trie_adj_list[0]:
    failure[neighbor] = 0

for u in bfs_order:
    if u != 0:
        for v in trie_adj_list[u]:
            c = trie[(u, v)]
            u2 = failure[u]
            has = -1
            flag = False
            while flag == False:
                for v2 in trie_adj_list[u2]:
                    if trie[(u2, v2)] == c:
                        has = v2
                        break
                if has != -1:
                    failure[v] = has 
                    flag = True
                else:
                    if u2 != 0:
                        u2 = failure[u2]
                    else:
                        flag = True
            if has == -1:
                failure[v] = 0                 
     
set1 = {}
for v in failure.values():
    if v != 0:
        set1[v] = []

for u in failure.keys():
    if failure[u] != 0:
        set1[failure[u]].append(u)

set2 = {}
for key in set1.keys():
    counter = 0
    for value in set1[key]:
        if end_of_word[value] == True:
            if counter == 0:
                set2[key] = []
            counter += 1
            set2[key].append(value)
s1 = {}

for u in trie_adj_list.keys():
    if u in set1.keys():
        min = pmin
        for u2 in set1[u]:
            k = depth[u2] - depth[u]
            if k < min:
                min = k
        s1[u] = min
    else:
        if u != 0:
            s1[u] = pmin
        else:
            s1[u] = 1

child_parent = {}
for key, value in trie_adj_list.items():
    for child in value:
        child_parent[child] = key
        
s2 = {}
for u in trie_adj_list.keys():
    if u in set2.keys():
        min = s2[child_parent[u]]
        for u2 in set2[u]:
            k = depth[u2] - depth[u]
            if k < min:
                min = k
        s2[u] = min
    else:
        if u == 0:
            s2[u] = pmin
        else:
            s2[u] = s2[child_parent[u]]

def has_child(trie, u, letter):
    haschild = False
    for child in trie_adj_list[u]:
        if trie[(u, child)] == letter:
            haschild = True
    return haschild

def get_child(trie, u, letter):
    find_it = False
    while not find_it:
        for child in trie_adj_list[u]:
            if trie[(u, child)] == letter:
                find_it = True
                return child

def commentz_walter_algorithm(t):
    q = deque()
    i = pmin - 1
    j = 0
    u = 0
    m = ''
    while i < len(t):
        while has_child(trie, u, t[i - j]):
            u = get_child(trie, u, t[i - j])
            m = m + t[i - j]
            j += 1
            if end_of_word[u] == True:
                m = m[::-1]
                q.append((m, i-j+1))
        if j > i:
            j = i
        first_part = s2[u]
        x = s1[u]
        y = rt[ordinal[t[i-j]]] - j - 1
        if x > y:
            second_part = x
        else:
            second_part = y
        if first_part < second_part:
            s = first_part
        else:
            s = second_part
        i = i + s
        j = 0
        u = 0
        m = ''
    return q
q = commentz_walter_algorithm(text)
if args.v:
    for i in range(len(bfs_order)):
        print(i, ":", s1[i], ",", s2[i])
for combination in q:
    print(combination[0], ":", combination[1])