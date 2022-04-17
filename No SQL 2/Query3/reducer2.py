import sys

count_dept_dict = {}
adjacency_square_matrix = [[0 for i in range(40)] for j in range(40)]

def multiplyRowColumn(row_list, column_list):
    sum = 0

    for i in range(40):
        sum += row_list[i]*column_list[i]

    return sum


for line in sys.stdin:
    # Read row and column indices and values
    row_data, column_data = line.split('\t')
    row, row_values = row_data.split("  ")
    column, column_values = column_data.split("  ")

    row = int(row)
    column = int(column)

    # Prepare row values
    row_values = row_values.strip('[').strip(']').split(',')
    row_values = [int(x) for x in row_values]

    # Prepare column values
    column_values = column_values.strip('[').strip('\n').strip(']').split(',')
    column_values = [int(x) for x in column_values]

    # Calculation of matrix square
    adjacency_square_matrix[row][column] = multiplyRowColumn(row_values, column_values)
   
# Printing result for common nodes
for row in range(40):
    for column in range(row + 1, 40):           
        if adjacency_square_matrix[row][column] != 0:
            print (row, column, adjacency_square_matrix[row][column])


print("Any node pair not present in this file has no common nodes ")