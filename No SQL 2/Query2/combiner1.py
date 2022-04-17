import sys

dept_pair_dict = {}

for line in sys.stdin:
    # Read data from mapper
    line = line.strip()

    dept_1 , dept_2 = line.split('\t')

    dept_2 = int(dept_2)
    dept_1 = int(dept_1)

    # Node pairs in non-decreasing order
    if dept_2 > dept_1:
        dept_pair = str(dept_1) + " " + str (dept_2)
    else:
        dept_pair = str(dept_2) + " " + str (dept_1)


    # collating all dept pairs to which dept sent mail
    if dept_pair not in dept_pair_dict:
        dept_pair_dict[dept_pair] = 1
    else:
        dept_pair_dict[dept_pair] += 1

# Number of distinct depts to which mail was sent
for key, val in dept_pair_dict.items():
    print (f'{key}\t{val}')