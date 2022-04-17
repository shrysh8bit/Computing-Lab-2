import sys

dept_pair_dict = {}
adjacency_matrix = [[0 for i in range(40)] for j in range(40)]

for line in sys.stdin:
    # Read dept and depts to whom mail has been sent
    from_dept, to_depts = line.split('\t')

    # Received data processing
    to_depts = to_depts.lstrip('{').rstrip('\n').rstrip('}')
    to_depts_list = to_depts.split(',')
    to_depts_list = [int(x) for x in to_depts_list]
   
    from_dept = int(from_dept)
    
    
    # Create adjaceny matrix
    for node in to_depts_list:
        adjacency_matrix[from_dept][node] = 1
        adjacency_matrix[node][from_dept] = 1

# Print row, column values above diagonal since matrix is symmetric
for row in range(40):
    for column in range(row + 1, 40):
        print (f'{row}  {adjacency_matrix[row]}\t{column}  {adjacency_matrix[column]}')