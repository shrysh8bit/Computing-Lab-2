import sys

email_edges_filename = 'network.txt'
employee_to_dept_file = 'dept_labels.txt'


with open (employee_to_dept_file, 'r') as dept_file:
    employee_to_dept = dept_file.read()
    employee_to_dept_list = employee_to_dept.split('\n')

employee_to_dept_list = employee_to_dept_list[:-1]


for item in employee_to_dept_list:
    print (f' {item}\t{1}')



with open (email_edges_filename, 'r') as file:
    email_edges = file.read()
    email_edges_list = email_edges.split('\n')

email_edges_list = email_edges_list[:-1]

for item in email_edges_list:
    print(f'{item}\t{1}')
