import sys

top_10_employee_file = '../Query2/Task2.txt'
email_edges_filename = 'network.txt'

with open (top_10_employee_file, 'r') as file:
    top_10_employee_str = file.read()
    top_10_employee_list = top_10_employee_str.split('\n')

top_10_employee_list = top_10_employee_list[:-1]

for item in top_10_employee_list:
    print(f'{item.split()[0]}   1')


with open (email_edges_filename, 'r') as file:
    email_edges = file.read()
    email_edges_list = email_edges.split('\n')

email_edges_list = email_edges_list[:-1]

for item in email_edges_list:
    if item.split()[0] != item.split()[1]:
        print(f'{item.split()[1]}\t1')