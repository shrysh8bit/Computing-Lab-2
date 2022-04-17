import sys

mail_send_count = {}
i = 0

for line in sys.stdin:
    if i < 10:
        i += 1
    else:
        break

    from_employee, count = line.split()
    mail_send_count[from_employee] = 0


for line in sys.stdin:
    to_employee, count = line.split()

    if to_employee in mail_send_count:
        mail_send_count[to_employee] += 1


for key, val in mail_send_count.items():
    line = str(key) + " " + str(mail_send_count[key])
    print(line)