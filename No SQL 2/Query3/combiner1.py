import sys

dept_pair_dict = {}

for line in sys.stdin:
    # Receive dept pairs
    dept_1 , dept_2 = line.split('\t')
    dept_2 = int(dept_2.strip("\n"))
    dept_1 = int(dept_1)

    # collating all depts to which dept sent mail
    if dept_1 not in dept_pair_dict:
        dept_pair_dict[dept_1] = [dept_2]
    else:
        dept_pair_dict[dept_1].append(dept_2)

    if dept_2 not in dept_pair_dict:
        dept_pair_dict[dept_2] = [dept_1]
    else:
        dept_pair_dict[dept_2].append(dept_1)

# Dept and depts to whom mail sent
for key, val in dept_pair_dict.items():
    print (f'{key}\t{set(val)}')