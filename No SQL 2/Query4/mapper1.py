import sys

mail_comunications = {}

for line in sys.stdin:
    # pair of depts who exch more than 50 mails
    line = line.strip('\n').strip('\r')
    mail_pair = line.split('\n')

    dept_1, dept_2 = mail_pair[0].split()

    if (dept_1 != dept_2):
        print (f'{dept_1}\t{dept_2}')
        # print (f'{dept_2}\t{dept_1}')
