import sys

dept_pair_dict = {}

for line in sys.stdin:
    line = line.strip()

    dept_1 , dept_2 = line.split('\t')
    dept_2 = int(dept_2)
    dept_1 = int(dept_1)

    dept_pair = str(dept_1) + " " + str(dept_2)
    dept_pair_reverse = str(dept_2) + " " + str(dept_1)
    # print (f'!{dept_1}!{dept_2}!')
    # collating all depts to which dept sent mail
    if dept_pair not in dept_pair_dict:
        dept_pair_dict[dept_pair] = 1
    else:
        dept_pair_dict[dept_pair] += 1

    if dept_pair_reverse not in dept_pair_dict:
        dept_pair_dict[dept_pair_reverse] = 1
    else:
        dept_pair_dict[dept_pair_reverse] += 1

for key, val in dept_pair_dict.items():
    print (f'{key}\t{(val)}')