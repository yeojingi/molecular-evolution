def limb_length(matrix, j):
    n = len(matrix)
    res = math.inf

    for i in range(n):
        for k in range(n):
            if k == j or i == j or i == k:
                continue

            D = (matrix[j][i]  + matrix[j][k] - matrix[i][k]) // 2

            res = min(D, res)
    
    return res

def additive_phylogeny(D):
    n = len(D)
    if n == 2:
        return [0, 1, D[0][1]]

    limbLength = limb_length(D, n-1)
    for j in range(n - 1):
        D[j][n-1] = D[j][n-1] - limbLength
        D[n-1][j] = D[j][n-1]
    


fn = "1.txt"
f = open(f"./data/{fn}", 'r')
N = int(f.readline().strip())
D = [ list(map(int, f.readline().strip())) for _ in range(N) ]
edges = additive_phylogeny(D)

for edge in edges:
    print(f"{edge[0]}->{edge[1]}:{edge[2]}")