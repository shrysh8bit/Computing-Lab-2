
email_edges_filename = 'network.txt'

with open (email_edges_filename, 'r') as file:
    email_edges = file.read()
    email_edges_list = email_edges.split('\n')
    email_edges_list = email_edges_list[:-1]

for line in email_edges_list:  
    line = line.strip()
    employee = line.split(" ")

    if employee[0] != employee[1]:
        print(f'{line}\t1')