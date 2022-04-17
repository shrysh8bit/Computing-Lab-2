import sys

adjacency_matrix = []
count = 0
node_list = []



for line in sys.stdin:
    node, adj_str = line.split('\t')
    
    node = int(node)
    adj_list = adj_str.strip().strip('[').strip(']').split(',')
    adj_list = [int(x) for x in adj_list]
    
    for i in range(42):
        if adj_list[i] == 0:
            adj_list[i] = 999
    
    # print (node, len(adj_list))
    
    adjacency_matrix.append(adj_list)
    
    if count >= 41:
        break
    else:
        count += 1
    
for line in sys.stdin:
    max, min1, min2 = line.split()
    max = int(max)

    for i in range(42):
        node_list.append(i)

    maxm = str(max) + " " + str(node_list[0]) + " " + str(node_list[1]) + " " + str(min1)
    minm = str(max) + " " + str(node_list[2]) + " " + str(node_list[4]) + " " + str(min2)

print (max, min1, min2)
print (maxm)
print (minm)

for i in range (42):
    if i != max:
        for j in range(42):
            if adjacency_matrix[max][i] + adjacency_matrix[i][j] < adjacency_matrix[max][j]:
                adjacency_matrix[max][j] = adjacency_matrix[max][i] + adjacency_matrix[i][j]
    print (f'{i}\t{adjacency_matrix[i]}')

# for row in range(42):

# print (adjacency_matrix[36][41])