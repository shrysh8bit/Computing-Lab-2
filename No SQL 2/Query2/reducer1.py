import sys

dept_comn_dict = {}

for line in sys.stdin:
    # Read node and depts with which comn
    line = line.strip()
    dept_pair, count = line.split('\t')

    count = int(count)

    # Summing up dept pair comn
    if dept_pair not in dept_comn_dict:
        dept_comn_dict[dept_pair] = count
    else:
        dept_comn_dict[dept_pair] += count

# Print node pairs with more than or equal to 50 mails exchanged 
for key, val in dept_comn_dict.items():
    if val >= 50:
        print (f'{key}')
