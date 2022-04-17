import sys

top_ten_employee_mail = [(0,0)]*10

for line in sys.stdin:
    employee_mail, line_count = line.split('\t')
    from_employee, mail_count = employee_mail.split()
    
    mail_count = int(mail_count)

    if mail_count > top_ten_employee_mail[-1][1]:
        for index in range(10):
            if mail_count > top_ten_employee_mail[index][1]:
                top_ten_employee_mail.insert(index, (from_employee, mail_count))
                top_ten_employee_mail.pop()
                break

for employee_mail_tuple in top_ten_employee_mail:
    print(employee_mail_tuple[0])