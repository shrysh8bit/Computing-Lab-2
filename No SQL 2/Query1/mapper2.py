import sys

from nbformat import from_dict

count_dept_dict = {}

for line in sys.stdin:
    line = line.strip()
    # Splitting dept and num of depts in contact
    from_dept, count = line.split('\t')

    # Print dept and no of distict depts to whom mail sent
    print (f'{from_dept}\t{count}')