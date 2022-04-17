import sys

count_dept_dict = {}

for line in sys.stdin:
    # Read dept and mail data
    line = line.strip()

    from_dept, to_depts_str = line.split('\t')

    # Count depts using num of mail sent as key
    if to_depts_str not in count_dept_dict:
        count_dept_dict[to_depts_str] = 1
    else:
        count_dept_dict[to_depts_str] += 1

# Print mails sent and num of such depts
for key, val in count_dept_dict.items():
    print (key, val)