import math

def limb_length(n, j, matrix):
    res = math.inf

    for i in range(n):
        for k in range(n):
            if k == j or i == j or i == k:
                continue

            D = (matrix[j][i]  + matrix[j][k] - matrix[i][k]) // 2

            res = min(D, res)
    
    return res

fn = "dataset_10329_11.txt"
f = open(f"./data/{fn}", "r")
n = int(f.readline().strip())
j = int(f.readline().strip())
matrix = [ list(map(int, f.readline().strip().split())) for _ in range(n) ]
res = limb_length(n, j, matrix)
print(res)