
task1_output = '../Query1/Task1.txt'

with open (task1_output, 'r') as file:
    email_edges = file.read()
    email_edges_list = email_edges.split('\n')

email_edges_list = email_edges_list[:-1]

for item in email_edges_list:
    print(f'{item}\t{1}')
