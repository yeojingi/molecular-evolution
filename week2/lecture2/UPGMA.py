from copy import deepcopy
import math

def find_closest_clusters(D):
    d = math.inf
    mi = 0
    mj = 0

    for i in range(len(D)):
        for j in range(len(D[0])):
            if D[i][j] < d:
                mi = i
                mj = j
    
    return [mi, mj, d]

def upgma(D, n):
    clusters = [ [i] for i in range(n) ]
    T = [ i for i in range(n) ]
    Age = [0] * n
    D_cluster = deepcopy(D)

    while len(clusters) > 1:
        [mi, mj, md] = find_closest_clusters(D_cluster)
        I = clusters[mi]
        J = clusters[mj]
        # merge Ci, Cj into C_new
        C_new = clusters[mi] + clusters[mj]
        clusters.append(C_new)
        # add a new node
        T.append(len(T))
        # remove cluster, T
        a, b = mj, mi if mi > mj else mi, mj
        clusters.pop(b)
        clusters.pop(a)
        T.pop(b)
        T.pop(a)
        D_cluster.pop(b)
        D_cluster.pop(a)
        for d in D_cluster:
            d.pop(b)
            d.pop(a)
        
        # connect C_new to Ci and Cj
        for k in range(len(D_cluster) - 1):
            # connect C_new and Ck
            D_k_new = 0

            Ck = clusters[k]
            for m in Ck:
                for i in I:
                    D_k_new += D[i][m] * len(I)

                for j in J:
                    D_k_new += D[j][m] * len(J)
                
            D_k_new /= (len(I) + len(J))
        
        # Age[mi] = 