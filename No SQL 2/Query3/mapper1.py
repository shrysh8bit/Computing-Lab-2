import sys

for line in sys.stdin:
    # Read pair of depts who exch more than 50 mails
    line = line.strip('\n').strip('\r')
    mail_pair = line.split('\n')

    dept_1, dept_2 = mail_pair[0].split()

    # Print the dept pairs for combiner
    if (dept_1 != dept_2):
        print (f'{dept_1}\t{dept_2}')
        # print (f'{dept_2}\t{dept_1}')
