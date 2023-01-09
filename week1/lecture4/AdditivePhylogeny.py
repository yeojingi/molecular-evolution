import math
from copy import deepcopy

def LimbLength(N, matrix):
  n = len(matrix)

  min_score = math.inf

  for i in range(n):
    for j in range(n):
      if i == j or i == N or j == N:
        continue

      min_score = min(min_score, 
        (matrix[N][i] + matrix[N][j] - matrix[i][j]) // 2,
      )

  return min_score

def FindPath(tree, node_i, node_k, x):
  edges = {}

  for edge in tree:
    if edges.get(edge[0]):
      edges[edge[0]].append([edge[1], edge[2]])
    else:
      edges[edge[0]] = [[edge[1], edge[2]]]
    
    if edges.get(edge[1]):
      edges[edge[1]].append([edge[0], edge[2]])
    else:
      edges[edge[1]] = [[edge[0], edge[2]]]

  stack = [[node_i, 0]]

  while stack:
    [cur, d] = stack.pop()
    print('cur, d, x', cur, d, x)
    if d == x:
      return [True, cur]
    if d > x:
      return [False, node_i, cur, d]

    if cur == node_k:
      return [False, node_i, node_k, d]
    
    if not edges.get(cur):
      return [False, node_i, node_k, d]

    for next in edges[cur]:
      stack.append([next[0], d + next[1]])
  
  return [False, node_i, node_k, d]

# It's helpful to think the process starting from the most bottom level recursion and then proceed up
# N is the number of leaves in the initial input matrix -
# new internal nodes will have label beginning from N, increasing by 1
def AdditivePhylogeny(matrix, N):

  n = len(matrix)

  if n == 2:
    tree = [[0, 1, matrix[0][1]]]

    # Return tree consisting of a single edge of length = matrix[0][1]
    return tree, N

  # Limb length of the leaf corresponding to the last row (n - 1) of the matrix
  limb_length = LimbLength(n - 1, matrix)
  print(limb_length, n-1)

  # Make matrix bald (subtract limb_length from the last row and col - except the diagonal element)
  for i in range(n-1):
    matrix[i][n-1] -= limb_length
    matrix[n-1][i] -= limb_length
  
  # Find two leaves i (node_i), k (node_k) such that matrix[i][k] = matrix[i][n - 1] + matrix[n - 1][k] (If there are multiple such nodes, I think any of them would work)
  for i in range(n-1):
    for k in range(n-1):
      if i == k:
        continue

      if matrix[i][k] == matrix[i][n-1] + matrix[n-1][k]:
        node_i = i
        node_k = k
        break

  # Distance from node_i to node (n - 1)
  x = matrix[node_i][n - 1]

  # Trim matrix (remove the last row and col)
  new_matrix = deepcopy(matrix[:-1])
  for i in range(n-1):
    new_matrix[i].pop()
  
  # Tree constructed from the trimmed matrix
  tree, new_node_label = AdditivePhylogeny(new_matrix, N)
  
  # Find path between node_i and node_k in the tree (Dijkstra algorithm)
  path = FindPath(tree, node_i, node_k, x)

  print('path', path, tree, node_i, node_k, n, x, limb_length)
  # Find node v with distance x from node_i on the path between node_i and node_k (if it exists)
  if path[0] == True:
    # Connect leaf (n - 1) to node v with weight = limb_length, and add this edge to the tree
    print('hi')
  # Else if there is no such node in the path, add a new internal node v (label beginning from N, increasing by 1) between node p and node q, where path length to p < x < path length to q
  else:
    v = new_node_label
    p = path[1]
    q = path[2]
    # Connect leaf (n - 1) to node v with weight = limb_length, and add this edge to the tree

    tree.append([n-1, v, limb_length])
    
    # Remove the edge between node p and node q
    for i in range(len(tree)):
      if (tree[i][0] == p and tree[i][1] == q) or (tree[i][1] == p and tree[i][0] == q):
        print('deleted', tree[i])
        break
    print('tree', tree)
    print(matrix)
    tree.pop(i)

    if p >= 0 and p < n:
      tree.append([p, v, matrix[p][n-1]])
      tree.append([q, v, path[3] - matrix[p][n-1]])
    else:
      tree.append([q, v, matrix[q][n-1]])
      tree.append([p, v, path[3] - matrix[q][n-1]])

    # # Then add new edge formed by adding node v (p to v)
    # tree.append([p, v, matrix[p][n-1]])
    
    # # Then add new edge formed by adding node v (v to q)
    # tree.append([q, v, matrix[q][n-1]])
    
    # Increase new_node_label by 1 for adding another internal node in the next round
    new_node_label+=1
    print('tree', tree)
      
  return tree, new_node_label

fn = "t.txt"
f = open(f"./data/{fn}", "r")
N = int(f.readline().strip())
matrix = [ list(map(int, f.readline().strip().split())) for _ in range(N) ]
res = AdditivePhylogeny(matrix, N)
ress = []
for edge in res[0]:
  ress.append([edge[0], edge[1], edge[2]])
  ress.append([edge[1], edge[0], edge[2]])
ress
ress.sort(key= lambda x : (x[0], x[1]))
for edge in ress:
  print(f"{edge[0]}->{edge[1]}:{edge[2]}")
  # print(f"{edge[1]}->{edge[0]}:{edge[2]}")
