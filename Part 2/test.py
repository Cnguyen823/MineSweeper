import ttg

clue1 = (True and False) or (False and True)
from itertools import product, permutations

def clue1(A,B): 
    return (A and (not B)) or ((not A) and B)

def clue2(A, B, C):
    return (A and (not B) and (not C)) or ((not A) and (not B) and C) or ((not A) and B and (not C))



# A, B, C

#clue 2
two = [['A', 1], ['B', 1], ['C', 1], ['A', 0], ['B', 0], ['C', 0]]

answer = []
final = []


inputs = permutations([two[0], two[1], two[2], two[3], two[4], two[5]], 3) 
for i in inputs: 
    if(i[0][1] + i[1][1] + i[2][1] == 1):
        temp = [i[0][0], i[1][0], i[2][0]]
        # print(temp)
        if(len(set(temp)) == len(temp)):
            answer.append(i)

print(answer)

for x in range(0, len(answer)):
    if answer[x][0][0] == 'A' and answer[x][1][0] == 'B' and answer[x][2][0] == 'C':
        final.append(answer[x])

print(final)
print(len(final))

# inputs = permutations([1, 0, 0], 3)
# for i in inputs:
#     if True:
#         print(i[0], i[1], i[2]) 

# table = ttg.Truths(['p', 'q'], ['p => q', 'p = q'])

# print(table)