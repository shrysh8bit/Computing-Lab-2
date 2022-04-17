import sys

dept_comn_dict = {}

for line in sys.stdin:
    # read from dept and to depts whom mail was sent
    line = line.strip()
    # print (repr(line))

    # Data pre processing
    from_dept, to_dept = line.split('\t')

    to_dept = to_dept.lstrip('{').rstrip('}')
    to_dept_list = to_dept.strip().split(',')
    to_dept_list = [int(x) for x in to_dept_list]
    
    # Collating data across event files
    if from_dept not in dept_comn_dict:
        dept_comn_dict[from_dept] = to_dept_list
    else:
        for element in to_dept_list:
            dept_comn_dict[from_dept].append(element)

# Dept and number of depts in comn
for key, val in dept_comn_dict.items():
    print (f'{key}\t{len(set(val))}')
