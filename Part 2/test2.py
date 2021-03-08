# {(((7, 0), 1), ((7, 1), 0), ((7, 2), 1)),
#  (((7, 0), 0), ((7, 1), 1), ((7, 2), 1)),
#   (((7, 0), 1), ((7, 1), 1), ((7, 2), 0))}

#   (7,2) = True

#   {(((7, 0), 0), ((7, 1), 1)), 
# (((7, 0), 1), ((7, 1), 0))}

#   {(((7, 0), 1), ((7, 1), 0),
#  (((7, 0), 0), ((7, 1), 1),
#   (((False)}

inference1 = {(((7, 0), 0), ((7, 1), 1)), (((7, 0), 1), ((7, 1), 0))}
inference2 = {(((7, 0), 1), ((7, 1), 0), ((7, 2), 1)), (((7, 0), 0), ((7, 1), 1), ((7, 2), 1)), (((7, 0), 1), ((7, 1), 1), ((7, 2), 0))}
print(inference1)
print(inference2)
(7,0), (7,1)
(7,0), (7,1), (7,2)

key = set()

for i in inference1:
    for j in inference2:
        print(i)
        print(j)
        if set(i).issubset(set(j)):
            print("Difference: ", set(j).difference(set(i)))
            key = set(j).difference(set(i))
            
        elif set(j).issubset(set(i)):
            key = set(i).difference(set(j))
        else:
            print(-1)

print(key)
test = tuple(key)

print(test[0])
for i in inference2:
    print(list(i))
    if test[0] in list(i):
        print("Ye")

if tuple(key) in inference2:
    print("Yo")