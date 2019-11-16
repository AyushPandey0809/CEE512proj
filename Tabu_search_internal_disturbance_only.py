# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from collections import defaultdict
import numpy as np
import math
import matplotlib.pyplot as plt
rnd=np.random
rnd.seed(4)

class node:
    def __init__(self, x, y,Type):
        self.x = x
        self.y = y
        self.type=Type

class edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.cost = ((start.x-end.x)**2+(start.y-end.y)**2)**(1/2)

class sol:
    def __init__(self, nodes, edges, total_cost):
        self.nodes = nodes      #array of nodes in solution
        self.edges = edges      #array of edges in solution
        self.total_cost = total_cost


# %%
##Type 1 = Hospitals
##type 2 = Green patients
##Type 3 = Red Patients
s0=[(0, 2), (0, 3),(1, 8), (2, 9), (3, 7), (4, 6), (5, 0), (6, 0), (7, 0), (8, 4), (9, 5)]
#initial solution 

n_g=6 #number of green patients
n_r=2 #number of red patients
n_h=2 #number of hospitals
n_k=3 #number of ambulances
total_nodes=n_g+n_r+n_h

G=[] #generating a graph to "fit" that initial solution, so i can test the disturbances

for i in range(total_nodes+1):
    if i<n_h:
        G.append(node(rnd.randint(20),rnd.randint(20),1))
    elif i>=n_h and i<n_h+n_g:
        G.append(node(rnd.randint(20),rnd.randint(20),2))
    else:
        G.append(node(rnd.randint(20),rnd.randint(20),3))

A=[(i,j) for i in range(total_nodes+1) for j in range(total_nodes+1) if i!=j] #set of arcs

E=[edge(G[i],G[j]) for i,j in A]

def cost_solution(solution):
    total_=0
    for i,j in solution:
        total_=total_+edge(G[i],G[j]).cost
    print(total_)


# %%
def sol_from_paths(paths):
    sol=[]
    for j in paths:
        for i in range(len(paths[j])-1):
            sol.append((paths[j][i],paths[j][i+1]))
    return sol

def extract_paths(solution): #FIX the empty dictionary
    sol=solution
    paths={i:[] for i in range(n_k)}
    while len(sol)>0:
        for j in range(n_k):
            for i in sol: 
                if G[i[0]].type==1 and len(paths[j])==0:
                    paths[j].append(i[0])
                    paths[j].append(i[1])
                    sol.remove(i)
                if len(paths[j])>0:
                    if i[0]==paths[j][-1]:
                        paths[j].append(i[1])
                        sol.remove(i)
                        if G[i[1]].type==1:
                            break
    sol=sol_from_paths(paths)
    return sol,paths


# %%
s0=[(0, 2), (0, 3),(1, 8), (2, 9), (3, 7), (4, 6), (5, 0), (6, 0), (7, 0), (8, 4), (9, 5)]
print(extract_paths(s0)[0])
s0=[(0, 2), (0, 3),(1, 8), (2, 9), (3, 7), (4, 6), (5, 0), (6, 0), (7, 0), (8, 4), (9, 5)]
xx=extract_paths(s0)[1]


# %%
def swapPositions(list, pos1, pos2): 
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def internal_patients_swap(paths): #swaps two green patients within the same route (path).
    paths=paths
    pos1=2295
    pos2=2295
    cnt=1
    while cnt>0:
        greens=[]
        i=rnd.randint(len(paths.keys()))
        for j in range(len(paths[i])):
            if G[paths[i][j]].type==2:
                greens.append(j) #index of green patients
        if len(greens)>1:
            while pos1==pos2:
                pos1=greens[rnd.randint(len(greens))]
                pos2=greens[rnd.randint(len(greens))]
            paths[i]=swapPositions(paths[i],pos1,pos2) #swaps two green patients in a path, guarantee to still be feasible
            sol=sol_from_paths(paths)
            return sol,paths


# %%



# %%
def internal_patients_relocate(paths): #changes the position of a green patient within one route (path). it is not allowed to be inserted after a red patient
    paths=paths
    pos1=2295
    pos2=2295
    cnt=1
    while cnt>0:
        greens=[]
        i=rnd.randint(len(paths.keys()))
        for j in range(len(paths[i])):
            if G[paths[i][j]].type==2:
                greens.append(j) #index of green patients
        if len(greens)>1:
            while pos1==pos2: 
                pos1=greens[rnd.randint(len(greens))] #index: relocate from
                pos2=greens[rnd.randint(len(greens))] #index: relocate to
            paths[i].insert(pos2,paths[i].pop(pos1)) #relocates the green patient from pos1 to pos2, it guarantees feasibility because we never try swapping with red code
            sol=sol_from_paths(paths)
            return sol,paths


# %%
s0=[(0, 2), (0, 3),(1, 8), (2, 9), (3, 7), (4, 6), (5, 0), (6, 0), (7, 0), (8, 4), (9, 5)]
cost_solution(s0)
new_sol=internal_patients_relocate(extract_paths(s0)[1])
cost_solution(new_sol[0])
print(new_sol[1])


# %%
def single_hospital_change(paths): #changes the destination hospital to an alternative hospital. We need to check feasibility for this one
    paths=paths
    hosp=[]
    i=rnd.randint(len(paths.keys()))
    for j in range(len(G)):
        if G[j].type==1:
            hosp.append(j)
    current=paths[i][-1]
    new=hosp[rnd.randint(len(hosp))]
    while current==new:
        new=hosp[rnd.randint(len(hosp))]
    paths[i][-1]=new
    sol=sol_from_paths(paths)
    return sol,paths


# %%
s0=[(0, 2), (0, 3),(1, 8), (2, 9), (3, 7), (4, 6), (5, 0), (6, 0), (7, 0), (8, 4), (9, 5)]
cost_solution(s0)
new_sol=single_hospital_change(extract_paths(s0)[1])
cost_solution(new_sol[0])
print(new_sol[1])


# %%



# %%



