from itertools import product 

def clue1(A,B): 
    return (A and (not B)) or ((not A) and B)

def clue2(A, B, C):
    return (A and (not B) and (not C)) or ((not A) and (not B) and C) or ((not A) and B and (not C))

#print(clue1(True, True)) 

#print(clue2(True, True, False))


def generate_logic(hiddenNeighbors, clue):
    
    return

neighbors = [(2,0), (2,1)]
generate_logic(neighbors, 1)



