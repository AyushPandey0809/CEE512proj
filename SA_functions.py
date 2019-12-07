#from collections import defaultdict
import numpy as np
#import math
import matplotlib.pyplot as plt
rnd=np.random
rnd.seed(5)

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


#s0=[(0,3), (3, 9),(9, 0), (0, 2), (2, 5), (5, 7), (7, 0), (0, 6), (6, 4), (4, 8), (8, 1)]
#initial solution

def cost_solution(G,solution): #given a set of arcs, it will give you the total cost (distance) which is NOT yet the time
    total_=0
    for i,j in solution:
        total_=total_+edge(G[i],G[j]).cost
    return total_

def sol_from_paths(paths): #it will divide each solution in their respective paths. A path or route is when an ambulance leaves and comes back to any hospital
    
    sol=[]
    for j in paths:
        for i in range(len(paths[j])-1):
            sol.append((paths[j][i],paths[j][i+1]))
    return sol

def extract_paths(G,solution): #SOLVE the empty dictionary
    nr=0
    for i in G:
        if i.type==3:
            nr=nr+1
    sol=solution
    paths={i:[] for i in range(nr)}
    while len(sol)>0:
        for j in range(nr):
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

def swapPositions(List, pos1, pos2): 
    List[pos1], List[pos2] = List[pos2], List[pos1] 
    return List
def swapPositionsExternal(List1, pos1,List2, pos2): 
    List1[pos1], List2[pos2] = List2[pos2], List1[pos1] 
    return List1,List2

def internal_patients_swap(G,paths): #swaps two green patients within the same route (path).
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

def internal_patients_relocate(G,paths): #changes the position of a green patient within one route (path). it is not allowed to be inserted after a red patient
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

def single_hospital_change(G,paths): #changes the destination hospital to an alternative hospital. We need to check feasibility for this one because of the capacity of hospitals 
    
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

def has_green(G,paths):
    green_exists=[]
    for i in paths.keys():
        green_count=0
        for j in paths[i]:
            if G[j].type==2:
                green_count=green_count+1
                break
        green_exists.append(green_count)
    return green_exists

def external_patients_relocate(G,paths): #chages one patient from route i to route k
    paths=paths
    pos1=2295
    pos2=2295
    green_exists=has_green(G,paths)
    greens_i=[] #stores indexes of green patients in path i
    greens_k=[] #stores indexes of green patients in path k
    i=1; k=1
    cnt=0
    if sum(green_exists)<1:
        return sol_from_paths,paths
    
    if sum(green_exists)==1:
       for j in range(len(green_exists)):
           if green_exists[j]==1:
               k=j
       i=rnd.randint(len(paths.keys()))
       while i==k:
           i=rnd.randint(len(paths.keys()))
    else:
        while cnt==0: #pick two different random paths   
            i=rnd.randint(len(paths.keys()))
            k=rnd.randint(len(paths.keys()))
            if i!=k and (green_exists[i]+green_exists[k]==2):
                cnt=1
    for j in range(len(paths[i])):
        if G[paths[i][j]].type==2:
            greens_i.append(j) #index of green patients in path i
    for j in range(len(paths[k])):
        if G[paths[k][j]].type==2:
            greens_k.append(j) #index of green patients in path k
    pos2=greens_k[rnd.randint(len(greens_k))] #index: relocate to
    
    if len(greens_i)==0:
        pos1=1
        paths[i].insert(pos1,paths[k].pop(pos2)) 
    else:
        pos1=greens_i[rnd.randint(len(greens_i))] #index: relocate from
        paths[i].insert(pos1,paths[k].pop(pos2)) 
    sol=sol_from_paths(paths)
    return sol,paths

def external_patients_swap(G,paths): #chages one patient from route i to route k
    paths=paths
    pos1=2295
    pos2=2295
    green_exists=has_green(G,paths)
    greens_i=[] #stores indexes of green patients in path i
    greens_k=[] #stores indexes of green patients in path k
    i=1; k=1
    cnt=0
    if sum(green_exists)<=1:
        return sol_from_paths(paths),paths
    
    else:
        while cnt==0: #pick two different random paths   
            i=rnd.randint(len(paths.keys()))
            k=rnd.randint(len(paths.keys()))
            if i!=k and (green_exists[i]+green_exists[k]==2):
                cnt=1
    for j in range(len(paths[i])):
        if G[paths[i][j]].type==2:
            greens_i.append(j) #index of green patients in path i
    for j in range(len(paths[k])):
        if G[paths[k][j]].type==2:
            greens_k.append(j) #index of green patients in path k
    pos2=greens_k[rnd.randint(len(greens_k))] #index: relocate to
    
    if len(greens_i)==0:
        pos1=1
    else:
        pos1=greens_i[rnd.randint(len(greens_i))] #index: relocate from
    swapPositionsExternal(paths[i],pos1,paths[k],pos2)
    sol=sol_from_paths(paths)
    return sol,paths




def external_path_swap(G,paths): #picks a green patient in path i and k, and anything after those patients get swapped
    paths=paths
    pos1=0
    pos2=0
    greens_i=[] #stores indexes of green patients in path i
    greens_k=[] #stores indexes of green patients in path k
    i=1; k=1
    cnt=1
    counter=0
    while cnt>0:
        while i==k: #pick two different random paths
            i=rnd.randint(len(paths.keys()))
            k=rnd.randint(len(paths.keys()))
        for j in range(len(paths[i])):
            if G[paths[i][j]].type==2:
                greens_i.append(j) #index of green patients in path i
        for j in range(len(paths[k])):
            if G[paths[k][j]].type==2:
                greens_k.append(j) #index of green patients in path k
        if len(greens_i)==0 or len(greens_k)==0:
            counter=counter+1
            rnd.seed(rnd.randint(5000))
            if counter>50:
                return sol_from_paths(paths),paths
            continue
        pos1=greens_i[rnd.randint(len(greens_i))] #index of path i
        pos2=greens_k[rnd.randint(len(greens_k))] #index of path k

        #switch everything going after each patient in their respective paths
        temp_i_first_half=[]
        temp_i_second_half=[]
        temp_k_first_half=[]
        temp_k_second_half=[]
        for l in range(len(paths[i])):
            if l<pos1: 
                temp_i_first_half.append(paths[i][l])
            else: 
                temp_i_second_half.append(paths[i][l])
        for l in range(len(paths[k])):
            if l<pos2: 
                temp_k_first_half.append(paths[k][l])
            else: 
                temp_k_second_half.append(paths[k][l])
        paths[i]=temp_i_first_half+temp_k_second_half
        paths[k]=temp_k_first_half+temp_i_second_half
        sol=sol_from_paths(paths)
        return sol,paths

def external_hospital_swap(paths): 
    #swaps the destination hospital of two routes. We need to check feasibility for this one because of the capacity of hospitals
    paths=paths
    i=1; k=1
    while i==k: #pick two different random paths
        i=rnd.randint(len(paths.keys()))
        k=rnd.randint(len(paths.keys()))
    paths[i][len(paths[i])-1],paths[k][len(paths[k])-1] = paths[k][-1], paths[i][-1]
    sol=sol_from_paths(paths)
    return sol,paths

def node_to_edge(s0):
    edges=[]
    for i in range(len(s0)-1):
        edges.append([s0[i],s0[i+1]])
    return edges

def plotting(G,s0):
    for i in G:
        if i.type==1:
            plt.scatter(i.x,i.y,c='black',marker='s')
        elif i.type==2:
             plt.scatter(i.x,i.y,c='g')
        else:
             plt.scatter(i.x,i.y,c='r')

    for i,j in s0:
        plt.plot([G[i].x, G[j].x], [G[i].y,G[j].y],c='b', alpha=0.5)
    for i in range(len(G)):
        plt.annotate((i),(G[i].x+200,G[i].y+200))
#    plt.axis('equal');

