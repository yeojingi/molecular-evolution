import math

def distance_between_leaves(N, matrix, M):
    dp = [ [[math.inf] * M for _ in range(M) ] for _ in range(M)]

    for i in range(M):
        for j in range(M):
            dp[i][j][0] = element(i, j, matrix)
            print(dp[i][j][0], end=" ")
        print()

    for k in range(1, M):
        for i in range(M):
            for j in range(M):
                dp[i][j][k] = min( dp[i][j][k-1], dp[i][k][k-1] + dp[k][j][k-1] )

    res = [ [0] * N for _ in range(N) ]

    for i in range(N):
        for j in range(N):
            res[i][j] = dp[i][j][M-1]
            if i == j:
                res[i][j] = 0
    
    return res

def element(i, j, matrix):
    if not matrix.get(i) or not matrix[i].get(j):
        return math.inf
    
    return matrix[i][j]

fn = "dataset_10328_12.txt"
f = open(f"./data/{fn}", "r")
N = int(f.readline().strip())
matrix = {}
M = 0 

while True:
    line = f.readline().strip()

    if not line:
        break
    
    [edge, d] = line.split(":")
    [s, e] = list(map(int, edge.split("->")))
    d = int(d)

    if s > M:
        M = s
    if e > M:
        M = e

    if matrix.get(s):
        matrix[s][e] = d
    else:
        matrix[s] = {e: d}

ress = distance_between_leaves(N, matrix, M+1)

for res in ress:
    print(*res, sep=" ")