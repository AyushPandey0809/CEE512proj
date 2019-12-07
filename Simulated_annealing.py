# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:57:18 2019

@author: jesusjo2
"""

#from collections import defaultdict
import numpy as np
import math as m
import copy
import matplotlib.pyplot as plt
from SA_functions import node
from SA_functions import edge
from SA_functions import sol_from_paths
from SA_functions import extract_paths
from SA_functions import cost_solution
from SA_functions import swapPositions
from SA_functions import internal_patients_swap
from SA_functions import internal_patients_relocate
from SA_functions import single_hospital_change
from SA_functions import external_patients_relocate
from SA_functions import external_patients_swap
from SA_functions import external_path_swap
from SA_functions import external_hospital_swap
from SA_functions import plotting
from SA_functions import node_to_edge
from SA_functions import has_green
from heuristic1 import partition
from heuristic1 import generateProb
from heuristic1 import get_part_h
from heuristic1 import heuristic
from heuristic1 import assign_in_partition
from heuristic1 import generateProb1
def generate_initial_solution(prob):
    idd={}
    j=0
    for i in prob.G:
        if i.type==1:
            idd[i]=j
            j=j+1
        elif i.type==2:
            idd[i]=j
            j=j+1
        else:
            idd[i]=j
            j=j+1
    
    routes=heuristic(prob.G,prob.E)
    initial_solution=[]
    for i in routes:
        for k in i:
            for j in k.E:
                initial_solution.append([idd[j.start],idd[j.end]])
    return initial_solution

def accept_solution(cost_disturbance,cost_current,k,T):
    delta=cost_current-cost_disturbance
    number=rnd.rand()
    if delta>=0:
        return 1
    else:
        acceptance_probability=1-m.exp(delta/(k*T))
        if number<acceptance_probability:
            print(number,acceptance_probability)
            return 1
        else:
            return 0



#ng=10
#nr=10
#nh=4
#
#prob=generateProb(ng,nr,nh)
##
#initial_solution=generate_initial_solution(prob)
##print(initial_solution)
#extract=extract_paths(prob.G,initial_solution)
#paths=extract[1]
#current_solution=extract[0]
#print(paths)
#print(has_green(prob.G,paths))
#current_cost=cost_solution(prob.G,current_solution)
#disturbance=external_patients_relocate(prob.G,paths)[0]
#prob = generateProb(ng, nr, nh)

#initial_sol=generate_initial_solution(prob)

#cost=cost_solution(prob.G,initial_sol)

loc_x=[44817.57441578,  9445.70483583,  2870.37771538, 19089.22995346,
       14541.16903042, 27984.01187448, 16152.51875086, 16076.24616334,
        5899.93938207, 13194.66793287, 48450.85860577, 13946.95385178,
       37898.4506986 , 45709.75380524, 42613.79666256, 11117.07076439,
        8830.4320609 ,  2466.09748081,  2081.4980608 , 10572.18675614,
       52723.09166399, 19683.15245571, 40154.94246345, 24999.45057367,
       26912.96814717, 49898.02842766,  5778.78303245, 24556.91888838,
        7474.11772276, 28424.81464189, 15787.12906321, 28392.94758531,
       35145.13399715, 19236.56067   , 32895.38310086, 33935.87394095,
       22175.04010114, 21291.20051574, 20614.1932179 , 21446.80678655,
        4206.37036459,  3000.68743456,  4135.87197583, 36731.78840175,
        1539.59313579, 26373.1997617 ,  7003.09197691,  1623.89745122,
       33765.04181497, 23548.70218904, 51459.23036599, 17411.64122922,
       10318.43066566, 36117.64001015, 18538.01966371, 40710.70678431,
       41807.01367231, 23436.57830582, 14194.13430644,  1262.15348448,
       19606.35947254,  5160.19044583, 38413.19056491, 24258.66565773,
       27482.21386995, 36145.24546531, 22455.32759144, 31863.37742603,
       44817.57441578,  9445.70483583,  2870.37771538]
loc_y=[11637.09553637,  5640.23601084,   634.13463323, 48467.30584881,
       33610.69611123, 11603.4355714 , 28910.76849651, 48618.22259433,
       46235.1617419 ,  6736.86578147, 16032.91746076, 15591.6589857 ,
       30048.74598753, 39252.5564358 , 17424.80178227, 32094.60182927,
       27227.65864623, 48565.47826011, 10632.15707058,    86.84320973,
        3787.5127876 , 22202.10941604, 26342.83723378, 30294.08905052,
       46483.71456855, 10598.01422086, 22238.20152946, 49224.24373896,
       19181.75413601,   792.21945527, 47505.60718522, 32493.12881324,
       51265.7412069 , 32821.55363934, 49434.65769086, 31629.29464977,
        7353.91616885, 35818.18538702, 28846.70169919,   477.54345058,
       40907.86866778,  6411.21385749, 27318.41072785, 35151.72375484,
       40281.7980314 , 49678.40489971,  6546.54340133, 11087.77496864,
       19291.41466938, 21188.03278606, 31152.28836222, 52478.69622483,
       32287.66852333, 36063.52732748,  5079.95629781, 22916.34425836,
        6819.57911181, 11373.29788829, 44883.48197729, 19535.43220813,
       12049.61890992, 45404.44398887, 24591.64112771, 35804.57607335,
       19951.85158974, 37827.69171914, 19273.04477469, 29120.35485712,
       11637.09553637,  5640.23601084,   634.13463323]




#

def Simulated_Annealing(ng,nr,nh):    
#     prob=generateProb1(loc_x,loc_y,ng,nr,nh)
     prob=generateProb(ng,nr,nh)
     initial_solution=generate_initial_solution(prob)
    #     first=copy.deepcopy(initial_solution)
     extract=extract_paths(prob.G,initial_solution)
     paths=extract[1]
     current_solution=extract[0]
     current_cost=cost_solution(prob.G,current_solution)
     best_cost=current_cost
     best=current_solution
     initial_cost=copy.deepcopy(best_cost)
     hospital=[0,1,2,2,2,3,4,5,5,5,6]
     green=[0,0,0,1,1,1,2,3,3,3,4,4,4,5,6,6,6]
     k=500000
     T=200
     iterations=25000
     for j in range(iterations):
         number=rnd.randint(2,7)
         if j>iterations*0.8 and nh>1:
             number=hospital[rnd.randint(len(hospital))]
         if j<iterations*0.2:
             number=green[rnd.randint(len(green))]
         if number==0:
             paths_before=copy.deepcopy(paths)
             solution_before=copy.deepcopy(current_solution)
             disturbance=internal_patients_swap(prob.G,paths)[0]
             new_cost=cost_solution(prob.G,disturbance)
             if accept_solution(new_cost,best_cost,k,T):
                 current_solution=disturbance
                 current_cost=new_cost
                 if T>5:
                     T=T/0.99
             else:
                 paths=copy.deepcopy(paths_before)
                 current_solution=copy.deepcopy(solution_before)
         elif number==1:
             paths_before=copy.deepcopy(paths)
             solution_before=copy.deepcopy(current_solution)
             disturbance=internal_patients_relocate(prob.G,paths)[0]
             new_cost=cost_solution(prob.G,disturbance)
  
             if accept_solution(new_cost,best_cost,k,T):
                 current_solution=disturbance
                 current_cost=new_cost
                 if T>5:
                     T=T/0.99
             else:
                 paths=copy.deepcopy(paths_before)
                 current_solution=copy.deepcopy(solution_before)
         elif number==2:
             if nh==1:
                 continue
             paths_before=copy.deepcopy(paths)
             solution_before=copy.deepcopy(current_solution)
             disturbance=single_hospital_change(prob.G,paths)[0]
             new_cost=cost_solution(prob.G,disturbance)
             if accept_solution(new_cost,best_cost,k,T):
                 current_solution=disturbance
                 current_cost=new_cost
                 if T>5:
                     T=T/0.99
             else:
                 paths=copy.deepcopy(paths_before)
                 current_solution=copy.deepcopy(solution_before)
         elif number==3:
             paths_before=copy.deepcopy(paths)
             solution_before=copy.deepcopy(current_solution)
             disturbance=external_patients_relocate(prob.G,paths)[0]
             new_cost=cost_solution(prob.G,disturbance)
             if accept_solution(new_cost,best_cost,k,T):
                 current_solution=disturbance
                 current_cost=new_cost
                 if T>5:
                     T=T/0.99
             else:
                 paths=copy.deepcopy(paths_before)
                 current_solution=copy.deepcopy(solution_before)
         elif number==4:
             paths_before=copy.deepcopy(paths)
             solution_before=copy.deepcopy(current_solution)
             disturbance=external_path_swap(prob.G,paths)[0]
             new_cost=cost_solution(prob.G,disturbance)
             if accept_solution(new_cost,best_cost,k,T):
                 current_solution=disturbance
                 current_cost=new_cost
                 if T>5:
                     T=T/0.99
             else:
                 paths=copy.deepcopy(paths_before)
                 current_solution=copy.deepcopy(solution_before)
         elif number==5:
             if nh==1:
                 continue
             paths_before=copy.deepcopy(paths)
             solution_before=copy.deepcopy(current_solution)
             disturbance=external_hospital_swap(paths)[0]
             new_cost=cost_solution(prob.G,disturbance)
             if accept_solution(new_cost,best_cost,k,T):
                 current_solution=disturbance
                 current_cost=new_cost
                 if T>5:
                     T=T/0.99
             else:
                 paths=copy.deepcopy(paths_before)
                 current_solution=copy.deepcopy(solution_before)
         elif number==6:
             paths_before=copy.deepcopy(paths)
             solution_before=copy.deepcopy(current_solution)
             disturbance=external_patients_swap(prob.G,paths)[0]
             new_cost=cost_solution(prob.G,disturbance)
             if accept_solution(new_cost,best_cost,k,T):
                 current_solution=disturbance
                 current_cost=new_cost
                 if T>5:
                     T=T/0.99
             else:
                 paths=copy.deepcopy(paths_before)
                 current_solution=copy.deepcopy(solution_before)
        
         if current_cost<best_cost:
             best=copy.deepcopy(current_solution)
             best_cost=cost_solution(prob.G,best)
             print(j,best_cost)
#         else:
#             current_solution=copy.deepcopy(first)
#             extract=extract_paths(prob.G,current_solution)
#             paths=extract[1]
     print("initial cost=", initial_cost)
     print("best cost= ",best_cost)
     extract=extract=extract_paths(prob.G,best)
     best=extract[0]
     best_path=extract[1]
#     print(paths)
#     print(first_paths)
     print(best_path)
#     plotting(prob.G,best)
     
     return prob,best

def max_path(cost_paths):
    max_cost=-1
    for i in cost_paths.keys():
        if cost_paths[i]>max_cost:
            max_cost=cost_paths[i]
            path=i
    return path
    


def feasible_hospital(G,best_paths):
    ambulances={}
    locations={}
    counter=0
    for i in range(n_k):
        ambulances[i]=[]
        locations[i]=i%n_h
    for i in best_paths.keys():
        for j in range(len(best_paths[i])):
            if len(ambulances[0])==0:
                ambulances[0].append(best_paths[i][j]) 
                continue
            if G[best_paths[i][j]].type!=1:
                ambulances[0].append(best_paths[i][j])   
                if G[best_paths[i][j]].type==3:
                    ambulances[0].append(locations[counter%n_h])
                    counter=counter+1
    return ambulances
                    
#                    for h in range(n_h):
#                        if edge(G[best_paths[i][j]],G[h]).cost<min_cost:
#                            min_cost=edge(G[best_paths[i][j]],G[h]).cost
#                            min_insertion=h
#                    ambulances[0].append(min_insertion)       
#    return ambulances



def paths_cost(G,pathz):
    cost_pathz={}
    for i in pathz:
        cost_pathz[i]=0
    for i in pathz:
        for j in range(len(pathz[i])-1):
            cost_pathz[i]=cost_pathz[i]+edge(G[pathz[i][j]],G[pathz[i][j+1]]).cost*(1/speed)
            if G[pathz[i][j]].type==2:
                cost_pathz[i]=cost_pathz[i]+d_i
            elif G[pathz[i][j]].type==3:
                cost_pathz[i]=cost_pathz[i]+d_i+d_h
    return cost_pathz


def ambulance_assignment(G,best_paths,cost_paths):
    ambulances={}
    locations={}
    for i in range(n_k):
        ambulances[i]=[]
        locations[i]=i%n_h
    sum_cost=sum(cost_paths[i] for i in cost_paths)
    empty_ambulances=n_k
    while sum_cost>1:
        for i in best_paths:
            for j in ambulances:
                if locations[j]==best_paths[i][0]:
                    if empty_ambulances==n_k or empty_ambulances==0:
                        for k in best_paths[i]:
                            ambulances[j].append(k)
                            if G[k].type==1: 
                                locations[j]=k
                                best_paths[i][0]=n_k
                        sum_cost=sum_cost-cost_paths[i]
                        empty_ambulances=max(empty_ambulances-1,0)
                    elif not ambulances[j]:
                        for k in best_paths[i]:
                            ambulances[j].append(k)
                            if G[k].type==1: 
                                locations[j]=k
                                best_paths[i][0]=n_k
                        sum_cost=sum_cost-cost_paths[i]
                        empty_ambulances=max(empty_ambulances-1,0)
    return ambulances,locations

def max_green(G,best_pathz):
    max_green=0
    cost_pathz={}
    for i in best_pathz:
        cost_pathz[i]=0
    for i in best_pathz:
        for j in range(len(best_pathz[i])-1):
            cost_pathz[i]=cost_pathz[i]+edge(G[best_pathz[i][j]],G[best_pathz[i][j+1]]).cost*(1/speed)
            if G[best_pathz[i][j]].type==2:
                cost_pathz[i]=cost_pathz[i]+d_i
                if cost_pathz[i]>max_green:
                    max_green=cost_pathz[i]
            elif G[best_pathz[i][j]].type==3:
                cost_pathz[i]=cost_pathz[i]+d_i+d_h
    return max_green

def max_red(G,best_pathz):
    max_red=0
    cost_pathz={}
    for i in best_pathz:
        cost_pathz[i]=0
    for i in best_pathz:
        for j in range(len(best_pathz[i])-1):
            cost_pathz[i]=cost_pathz[i]+(edge(G[best_pathz[i][j]],G[best_pathz[i][j+1]]).cost*(1/speed))
            if G[best_pathz[i][j]].type==2:
                cost_pathz[i]=cost_pathz[i]+d_i
            elif G[best_pathz[i][j]].type==3:
                cost_pathz[i]=cost_pathz[i]+d_i+d_h
                if cost_pathz[i]>max_red:
                    max_red=cost_pathz[i]
    return max_red


rnd=np.random
rnd.seed(2)
n_g=20
n_r=10
n_h=1
n_k=3
w_g=1
w_r=4
n_p=n_r+n_g
meta=Simulated_Annealing(n_g,n_r,n_h)


G=copy.deepcopy(meta[0].G)
E=copy.deepcopy(meta[0].E)
solution=copy.deepcopy(meta[1])
best_paths=extract_paths(G,solution)[1]
speed=3080# 35mpg=3080ft/min
d_i=5 #minutes
d_h=5 #minutes (time to drop at hospital)
cost_paths={}

new_solution=extract_paths(G,sol_from_paths(feasible_hospital(G,best_paths)))
best_paths=new_solution[1]
#print(cost_solution(G,sol_from_paths(best_paths)))
cost_paths=paths_cost(G,best_paths)

ccopy=copy.deepcopy(best_paths)

ambulances=ambulance_assignment(G,best_paths,cost_paths)[0]
print(ambulances)

#ambulances={}
#ambulances[0]=[0,14,1,6,12,0,13,0,3,5,9,1]
#ambulances[1]=[1,4,7,11,16,1,8,15,0,2,10,1]
Objective=max_green(G,ambulances)+max_red(G,ambulances)
print(Objective)

plotting(G,sol_from_paths(ambulances))
#plt.scatter(loc_x[0:n_h],loc_y[0:n_h], c='black',marker='s')
#plt.scatter(loc_x[n_h:n_h+n_g],loc_y[n_h:n_h+n_g],c='g')#green patients
#plt.scatter(loc_x[n_h+n_g:n_h+n_p],loc_y[n_h+n_g:n_h+n_p],c='r')
#for i in range(n_h+n_p):
#    plt.annotate((i),(loc_x[i]+200,loc_y[i]+200))
#plt.axis('equal');

       