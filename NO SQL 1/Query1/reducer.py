import sys
# import os

employee_mail_count = {}

for line in sys.stdin:
    mail_pair, count = line.split('\t')
    from_employee, to_employee = mail_pair.split()

    if from_employee != to_employee:
        if from_employee not in employee_mail_count:
            employee_mail_count[from_employee] = 1
        else:
            employee_mail_count[from_employee] += 1


# print(f"The number of mails sent by each employee is as follows")

# with open('Task1.txt', 'w') as file:

for from_employee, count in employee_mail_count.items():
    line = from_employee + " " + str(count)
    print(line)

# Copy ouput file to Task 2 folder for query 2
# os.system('cp ./Task1.txt ../Query2')