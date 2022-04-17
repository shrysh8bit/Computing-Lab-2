import sys


for line in sys.stdin:
    # read the row and column values
    line = line.strip()
    # Read dept and depts to whom mail has been sent
    rows, columns = line.split('\t')

    # Send the values to reducer2
    print (f'{rows}\t{columns}')