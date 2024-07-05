import argparse

parser = argparse.ArgumentParser()
parser.add_argument("method", help="The method that will be used for the clustering")
parser.add_argument("file", help="The file with the elemets for clustering")
args = parser.parse_args()
list1 = []
method = args.method
with open(args.file, 'r') as file:
    elements = file.read().strip()
    list1 = elements.split()
#clusters consists of the integer values of list1
clusters = []
for i in list1:
    clusters.append([int(i)])
clusters.sort()

#Initializes distances between the single element clusters
#and stores these distances in lists
#Takes as input the cluster list and outputs the distances list
distances = []
def initialize_distances(list1):
    i = 0
    while i < len(list1):
        j = 0
        list2 = []
        while j < len(list1):
            list2.append(float(abs(list1[i][0]-list1[j][0])))
            j = j + 1
        distances.append(list2)
        i = i + 1
    return distances

def merge_clusters(cluster1_index, cluster2_index):
    if cluster1_index > cluster2_index:
        cluster1_index , cluster2_index = cluster2_index , cluster1_index
    temp = []
    temp = clusters[cluster1_index] + clusters[cluster2_index]
    temp.sort()
    a = clusters[cluster1_index]
    b = clusters[cluster2_index]
    clusters.insert(cluster1_index, temp)
    clusters.remove(a)
    clusters.remove(b)

#Find min in clusters list. Ignore 0 as it measures the distance of a cluster from itself
def find_min_dist(list1):
    min_dist = float('inf')
    i = 0
    while i < len(list1):
        j = 0
        while j < len(list1[i]):
            if i == 0 and list1[i][j] != 0.0:
                min_dist = list1[i][j]
            if list1[i][j] != 0 and list1[i][j] < min_dist:
                min_dist = list1[i][j]
            j = j + 1
        i = i + 1
    return min_dist

#Find first index where min min_dist is observed in clusters list
def min_indexes(list1, m):
    i = 0 
    min_i = i
    flag1 = True
    while i < len(list1) and flag1:
        j = 0
        min_j = j
        flag2 = True
        while j < len(list1[i]) and flag2:
            if list1[i][j] == m:
                flag2 = False
                min_i = i
                min_j = j
            j = j + 1
        if flag2 == False:
            flag1 = False
        i = i + 1
    return min_i, min_j

def copy_list(list_parameter):
    list_parameter_copy = []
    for x in list_parameter:
        l1 = []
        for y in x:
            l1.append(y)
        list_parameter_copy.append(l1)
    return list_parameter_copy

def find_dist_s_v(distances_list, index_min_i, index_v):
    if index_min_i > index_v:
        index_min_i, index_v = index_v, index_min_i
    dist_s_v = distances_list[index_min_i][index_v]
    return dist_s_v

def find_dist_t_v(distances_list, index_min_j, index_v):
    if index_min_j > index_v:
        index_min_j, index_v = index_v, index_min_j
    dist_t_v = distances_list[index_min_j][index_v]
    return dist_t_v

def find_dist_s_t(distances_list, index_min_i, index_min_j):
    if index_min_i > index_min_j:
        index_min_i, index_min_j = index_min_j, index_min_i
    dist_s_t = distances_list[index_min_i][index_min_j]
    return dist_s_t

def dist_u_v(dist_s_v, dist_t_v, dist_s_t, ai, aj, b, g):
    return ai*dist_s_v + aj*dist_t_v + b*dist_s_t + g*abs(dist_s_v-dist_t_v)

def distance_single_method(dist_s_v, dist_t_v, dist_s_t):
    return dist_u_v(dist_s_v, dist_t_v, dist_s_t, 1/2, 1/2, 0, -1/2)

def distance_complete_method(dist_s_v, dist_t_v, dist_s_t):
    return dist_u_v(dist_s_v, dist_t_v, dist_s_t, 1/2, 1/2, 0, 1/2)

def distance_average_method(dist_s_v, dist_t_v, dist_s_t, len_s, len_t):
    ai = len_s/(len_s + len_t)
    aj = len_t/(len_s + len_t)
    b = 0
    g = 0
    return dist_u_v(dist_s_v, dist_t_v, dist_s_t, ai, aj, b, g)

def distance_ward_method(dist_s_v, dist_t_v, dist_s_t, len_s, len_t, len_v):
    ai = (len_s + len_v)/(len_s + len_v + len_t)
    aj = (len_t + len_v)/(len_s + len_v + len_t)
    b = -len_v/(len_s + len_v + len_t)
    g = 0
    return dist_u_v(dist_s_v, dist_t_v, dist_s_t, ai, aj, b, g)

def lance_williams_methods(clustering_list):
    distances = initialize_distances(clustering_list)
    distances_copy = copy_list(distances)
    while len(clustering_list) > 1:
        m = find_min_dist(distances)
        index_min_i, index_min_j = min_indexes(distances, m)
        v = 0
        for v in range(0, len(clustering_list)):
            a = distances[v][index_min_j]
            distances[v].pop(index_min_j)
        del distances[index_min_j]
        for v in range(0, len(clustering_list)):
            if v != index_min_i and v != index_min_j:
                dist_s_v = find_dist_s_v(distances_copy, index_min_i, v)
                dist_t_v = find_dist_t_v(distances_copy, index_min_j, v)
                dist_s_t = find_dist_s_t(distances_copy, index_min_i, index_min_j)
                if method == 'single':
                    dist_u_v = distance_single_method(dist_s_v, dist_t_v, dist_s_t)   
                elif method == 'complete':
                    dist_u_v = distance_complete_method(dist_s_v, dist_t_v, dist_s_t)
                elif method == 'average':
                    len_s = len(clustering_list[index_min_i])
                    len_t = len(clustering_list[index_min_j])
                    dist_u_v = distance_average_method(dist_s_v, dist_t_v, dist_s_t, len_s, len_t)
                elif method == 'ward':
                    len_s = len(clustering_list[index_min_i])
                    len_t = len(clustering_list[index_min_j])
                    len_v = len(clustering_list[v])
                    dist_u_v = distance_ward_method(dist_s_v, dist_t_v, dist_s_t, len_s, len_t, len_v)

                if v < index_min_i:
                    distances[index_min_i][v] = dist_u_v
                    distances[v][index_min_i] = dist_u_v
                else:
                    distances[index_min_i][v-1] = dist_u_v
                    distances[v-1][index_min_i] = dist_u_v  
            elif v == index_min_i:
                dist_u_v = 0
                distances[index_min_i][v] = dist_u_v
        distances_copy = copy_list(distances)
        sum = len(clustering_list[index_min_i])+len(clustering_list[index_min_j])
        str1 = " ".join(str(x) for x in clustering_list[index_min_i])
        str2 = " ".join(str(x) for x in clustering_list[index_min_j])
        m = "{:.2f}".format(m)
        print('(', str1, ') (', str2,')', m, sum)
        merge_clusters(index_min_i, index_min_j)
        
lance_williams_methods(clusters)










