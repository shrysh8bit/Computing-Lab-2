import sys

for line in sys.stdin:
    # pair of depts who exch a mail
    line = line.strip()
    # print (repr(line))

    dept_1, dept_2 = line.split()

    # if mail not sent to own dept, print dept pair
    if (dept_1 != dept_2):
        print (f'{dept_1}\t{dept_2}')
        # print (f'{dept_2}\t{dept_1}')
