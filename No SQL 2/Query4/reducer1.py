import sys

dept_pair_dict = {}
adjacency_matrix = [[0 for i in range(42)] for j in range(42)]

max_node = 0
length_max = 0

min_node1 = 0
min_node2 = 0
length_min = 42


for line in sys.stdin:
    dept_pair, count = line.split('\t')
    count = int(count)

    from_dept, to_dept = dept_pair.split()
    from_dept = int(from_dept)
    to_dept = int(to_dept)
   
    adjacency_matrix[from_dept][to_dept] = count
    adjacency_matrix[to_dept][from_dept] = count
    
    if from_dept not in dept_pair_dict:
        dept_pair_dict[from_dept] = 1
    else:
        dept_pair_dict[from_dept] += 1
  

for row in range(42):
    print (f'{row} \t{adjacency_matrix[row]}')
    # for column in range(row + 1, 40):
        # print (f'{row}  {adjacency_matrix[row]}\t{column}  {adjacency_matrix[column]}')


    # Find max dept commn mail node
    sum = 0
    for item in adjacency_matrix[row]:
        if item > 0:
            sum += 1

    length = sum
    # print(length)
    if length > length_max:
        max_node = row
        length_max = length


    # Find min dept commn mail nodes
    if length == length_min:
        min_node2 = row
    
    if length < length_min:
        min_node1 = row
        length_min = length

print (max_node, min_node1, min_node2)


# length = len(dept_mail_pair_list)
