import sys

employee_to_dept = {}
dept_mail_out = {}

i = 0

for line in sys.stdin:

    if i < 1005:
        i += 1
    else:
        break
    
    employee_id_dept, unused = line.split('\t')
    employee_id, dept = employee_id_dept.split()
    employee_to_dept[employee_id] = dept

for i in range(42):
    dept_mail_out[str(i)] = 0


max_mail_sent_dept = [0,0]
for line in sys.stdin:
    email_edge, unused = line.split('\t')
    from_employee, to_employee = email_edge.split()
    
    if from_employee != to_employee and employee_to_dept[from_employee] != employee_to_dept[to_employee]:
        dept_mail_out[employee_to_dept[from_employee]] += 1

        if dept_mail_out[employee_to_dept[from_employee]] > max_mail_sent_dept[1]:
            max_mail_sent_dept[0] = employee_to_dept[from_employee]
            max_mail_sent_dept[1] = dept_mail_out[employee_to_dept[from_employee]]


line = str(max_mail_sent_dept[0]) + " " + str(max_mail_sent_dept[1])
print(line)