from copy import deepcopy
import math

def find_closest_clusters(D):
    d = math.inf
    mi = 0
    mj = 0

    for i in range(len(D)):
        for j in range(len(D[0])):
            if i == j:
                continue

            if D[i][j] < d:
                mi = i
                mj = j
                d = D[i][j]
    
    return [mi, mj, d]

def upgma(D, n):
    clusters = [ [i] for i in range(n) ]
    T = [ i for i in range(n) ]
    Age = [0] * n
    D_cluster = deepcopy(D)

    while len(clusters) > 1:
        [mi, mj, md] = find_closest_clusters(D_cluster)
        print(clusters)
        print(*D_cluster, sep="\n")
        I = clusters[mi]
        J = clusters[mj]
        # merge Ci, Cj into C_new
        C_new = clusters[mi] + clusters[mj]
        clusters.append(C_new)
        # add a new node
        T.append(len(T))
        # remove cluster, T
        [a, b] = [mj, mi] if mi > mj else [mi, mj]

        print(a, b, md)

        clusters.pop(b)
        clusters.pop(a)
        # T.pop(b)
        # T.pop(a)
        D_cluster.pop(b)
        D_cluster.pop(a)
        for d in D_cluster:
            d.pop(b)
            d.pop(a)
        
        # connect C_new to Ci and Cj
        for k in range(len(D_cluster)):
            # connect C_new and Ck
            D_k_new = 0

            Ck = clusters[k]
            for m in Ck:
                for i in I:
                    D_k_new += D[i][m] * len(I) / len(Ck)

                for j in J:
                    D_k_new += D[j][m] * len(J) / len(Ck)
                
            print(D_k_new, 'knew', len(I) + len(J))
            D_k_new /= (len(I) + len(J))

            D_cluster[k].append(D_k_new)
        
        # for k in range(len(D_cluster)):
        #     d.append(D_k_new)
        D_cluster.append([ D_cluster[k][-1] for k in range(len(D_cluster))] + [0])

        Age[mi] = D_k_new / 2
    
    print(Age)
    return T

fn = "1.txt"
f = open(f"./data/{fn}", "r")
N = int(f.readline().strip())
matrix = [ list(map(int, f.readline().strip().split())) for _ in range(N) ]
res = upgma(matrix, N)
print(res)