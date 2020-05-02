# A Python program to print all
# combinations of given length
from itertools import combinations

# Get all combinations of [1, 2, 3]
# and length 2
comb = combinations(['a', 'b', 'c', 'd', 'e'], 2)

# Print the obtained combinations
for i in list(comb):
    print(i)
