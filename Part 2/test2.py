# {(((7, 0), 1), ((7, 1), 0), ((7, 2), 1)),
#  (((7, 0), 0), ((7, 1), 1), ((7, 2), 1)),
#   (((7, 0), 1), ((7, 1), 1), ((7, 2), 0))}

#   (7,2) = True

#   {(((7, 0), 0), ((7, 1), 1)), 
# (((7, 0), 1), ((7, 1), 0))}

#   {(((7, 0), 1), ((7, 1), 0),
#  (((7, 0), 0), ((7, 1), 1),
#   (((False)}

# inference1 = {(((7, 0), 0), ((7, 1), 1)), (((7, 0), 1), ((7, 1), 0))}
# inference2 = {(((7, 0), 1), ((7, 1), 0), ((7, 2), 1)), (((7, 0), 0), ((7, 1), 1), ((7, 2), 1)), (((7, 0), 1), ((7, 1), 1), ((7, 2), 0))}

inference2 = [[[(7, 0), 0], [(7, 1), 1]], [[(7, 0), 1], [(7, 1), 0]]]
inference1 = [[[(7, 0), 1], [(7, 1), 0], [(7, 2), 1]], [[(7, 0), 0], [(7, 1), 1], [(7, 2), 1]], [[(7, 0), 1], [(7, 1), 1], [(7, 2), 0]]]

# print(inference1)
# print(inference2)
temp2 = [(7,0), (7,1)]
temp1 = [(7,0), (7,1), (7,2)]

# print(temp1);
# print(temp2);

leastRecurring = set()
b = 0
checkInference = 0
checkList = []

if len(temp1) == len(temp2):
    print(-1)
elif set(temp1).issubset(set(temp2)):
    print("Difference: ", set(temp2).difference(set(temp1)))
    leastRecurring = tuple(set(temp2).difference(set(temp1)))
    checkList = list(inference2)
    checkInference = 1
elif set(temp2).issubset(set(temp1)):
    print("Difference: ", set(temp1).difference(set(temp2)))
    leastRecurring = tuple(set(temp1).difference(set(temp2)))
    checkList = list(inference1) 
    checkInference = 2
else:
    print(-1)

res = [list(ele) for ele in checkList]
# print(res)

delete = False 

for i in checkList:
    # print(i)
    for j in i:
        if j[0] == leastRecurring[0]:
            # print("Before:", j)
            if j[1] == b:
                j[1] = 1
            else:
                j[1] = 0
    


print(checkList)

checkList = [ i for i in checkList for j in i if j[0] == leastRecurring[0] and j[1] == 1]

for i in checkList:
    for j in i:
        if j[0] == leastRecurring[0]:
           i.remove(j)


print(checkList)

answer = False

if checkInference == 1:
    final = inference1
elif checkInference == 2:
    final = inference2

print("Final: ", final)

listToPost = []


for i in final:
    print(i)
    for j in checkList:
        if j == i:
            print("J[0]: ", j[0][0])
            print("B remains true")
            answer = True
            listToPost.append(j[0][0])
            break
    if answer == True:
        break

if answer == False:
    b = not b
    print(b)
    print("B is a contradiction")



# delete = False

# for i in checkList:
#     print(i)
#     for j in i:
#         if j[0] == leastRecurring[0]:
#             if j[1] == 0:
#                 delete = True
#             else:
#                 i.remove(j)

#     if delete == True:   
#         checkList.remove(i)
#         delete = False

# print(checkList)
