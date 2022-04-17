import sys
adjacency_matrix = []
max = 0
min1 = 0
min2 = 0
maxm = 0
minm = 0

count = 0
for line in sys.stdin:
    # print (repr(line))
    line_list = line.split()
    # print (line_list)
    line_list = [int(x) for x in line_list]
    if len(line_list) == 3:
        max = int(line_list[0])
        min1 = int(line_list[1])
        min2 = int(line_list[2])
    elif line_list[-1] == min1:
        maxm = line.strip()
        # print (count, line)
    else:
        minm = line.strip()
        # print (count, line)

    if count >= 2:
        break
    else:
        count += 1
    

for line in sys.stdin:
    line = line.strip()
    node, distances = line.split('\t')
    # print (repr(distances))

    node = int(node)
    adj_list = distances.strip('[').strip().strip(']').split(',')
    adj_list = [int(x) for x in adj_list]

    # print (type(adj_list))
    adjacency_matrix.append(adj_list)

print (maxm, adjacency_matrix[max][min1])
print (minm, adjacency_matrix[max][min2])
# for row in range(40):
#     for column in range(row + 1, 40):           
#         if adjacency_square_matrix[row][column] != 0:
#             print (row, column, adjacency_square_matrix[row][column])
