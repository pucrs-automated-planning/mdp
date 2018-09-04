import numpy as _np
import scipy.sparse as _sp

ACTIONS = ['N','S','E','W']


"""
input:
shape -> [Y,X] shape of the grid
obstacles -> [[Y1,X1], [Y2,X2]] list with the position of obstacles
terminals -> [[Y1,X1], [Y2,X2]] list with the position of terminal states
pm -> (0.0 - 1.0) the probability of successfully moving
r -> (double/int value) the default reward for all states
rewards -> [[Y1,X1,R1], [Y2,X2,R2]] a cell array of [Y,X,R] rewards for specific states

output: 
P = (A x S x S) the transition function
R = (A x S x S) the reward function
"""

def mdp_grid(shape=[], obstacles=[], terminals=[], pm=0.8, r=1, rewards=[]):
    S = shape[0] * shape[1]
    P = _np.zeros([4,S,S])
    Ps = (1-pm)/2
    for A in range(4):
        for I in range(shape[0]):
            for J in range(shape[1]):
                if [I,J] in obstacles:
                    #Sfrom = sub2ind(shape, I, J)
                    #P[A,Sfrom,Sfrom] = 1.0;
                    continue

                if [I,J] in terminals:
                    #Sfrom = sub2ind(shape, I, J)
                    #P[A,Sfrom,Sfrom] = 1.0;
                    continue
                
                Sfrom = sub2ind(shape, I, J)
                ti, tj = front(A,I,J)
                #If the destination of the move is out of the grid, add Pm to self transition
                if valid(ti,tj,shape,obstacles):
                    Sto = sub2ind(shape,ti,tj)
                    #print "Front Sfrom ", Sfrom, "Sto ", Sto
                    P[A,Sfrom,Sto] = pm;
                else:
                    P[A,Sfrom,Sfrom] = pm;
                
                #If any of the sides of the move are out of the grid, add Ps to self transition
                ti, tj = left(A,I,J);
                if valid(ti,tj,shape,obstacles):
                    Sto = sub2ind(shape,ti,tj)
                    P[A,Sfrom,Sto] = Ps
                else:
                    P[A,Sfrom,Sfrom] = P[A,Sfrom,Sfrom] + Ps
                
                ti, tj = right(A,I,J);
                if valid(ti,tj,shape,obstacles):
                    Sto = sub2ind(shape,ti,tj)
                    P[A,Sfrom,Sto] = Ps
                else:
                    P[A,Sfrom,Sfrom] = P[A,Sfrom,Sfrom] + Ps
                
    R = _np.ones([S]);
    R = _np.multiply(R,r)
    for i in range(len(rewards)):
        Si = rewards[i][0]
        Sj = rewards[i][1]
        Sv = rewards[i][2]
        SR = sub2ind(shape, Si,Sj)
        R[SR]=Sv
    RSS = r_to_rs(P,R,terminals,obstacles, shape)
    return(P, RSS)

# def r_to_rss(P, R, terminals, obstacles):
#     RSS = _np.zeros([4,len(P[1]),len(P[1])])
#     for A in range(4):
#         for I in range(len(P[1])):
#             for J in range(len(P[1])):
#                 if([I,J] in terminals):
#                     RSS[A,I,J] = R[J]
#                 if([I,J] in obstacles): RSS[A,I,J] = 0
#                 RSS[A,I,J] = (P[A,I,J] * R[J])
#     return RSS

def r_to_rs(P, R, terminals, obstacles, shape):
    RS = _np.zeros([len(P[1]),4])
    for I in range(len(P[1])):
        for A in range(4):
            sub = ind2sub(shape, I)
            #if sub in obstacles: RS[I,A] = 0
            if sub in terminals: RS[I,A] = R[I]
            else:
                for J in range(len(P[1])):
                    RS[I,A] = RS[I,A] + (P[A,I,J] * R[J])
    return RS

def sub2ind(shape, rows, cols):
    return rows*shape[1] + cols

def ind2sub(shape, ind):
    rows = int((ind / shape[1]))
    cols = int((ind % shape[1]))
    return [rows, cols]

def valid(I, J, shape, obstacles):
    valid = ((I >= 0) and (I < shape[0])) and ((J >= 0) and (J < shape[1]))
    valid = valid and (not [I,J] in obstacles)
    return valid

#Returns the "left" position of the specified position given Action
def left(A, I, J):
    if A == 0:
        D =[I,J-1]
    elif A == 1: 
        D = [I,J+1]
    elif A == 2:
        D = [I-1,J]
    elif A == 3:
        D = [I+1,J]
    else:
        print("Invalid action")
        return 0,0
    return D[0], D[1]

#Returns the "right" position of the specified position given Action
def right(A, I, J):
    if A == 0:
        D = [I,J+1]
    elif A == 1:
        D = [I,J-1]
    elif A == 2:
        D = [I+1,J]
    elif A == 3:
        D = [I-1,J]
    else:
        print("Invalid action")
        return 0,0
    return D[0], D[1]


#Returns the "front" position of the specified position given Action
def front(A, I, J):
    if A == 0:
        D = [I-1,J]
    elif A == 1:
        D = [I+1,J]
    elif A == 2:
        D = [I,J+1]
    elif A == 3:
        D = [I,J-1]
    else:
        print("Invalid action")
        return 0,0
    return D[0], D[1]

def print_policy(policy, shape, obstacles=[], terminals=[]):
    p_policy = _np.empty(shape, dtype=object)
    for i in range(len(policy)):
        sub = ind2sub(shape, i)
        if sub in obstacles: p_policy[sub[0]][sub[1]] = 'O'
        elif sub in terminals: p_policy[sub[0]][sub[1]] = 'T'
        else: p_policy[sub[0]][sub[1]] = ACTIONS[policy[i]]
    print(p_policy)
