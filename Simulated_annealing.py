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
from Tabu_functions import node
from Tabu_functions import edge
from Tabu_functions import sol_from_paths
from Tabu_functions import extract_paths
from Tabu_functions import cost_solution
from Tabu_functions import swapPositions
from Tabu_functions import internal_patients_swap
from Tabu_functions import internal_patients_relocate
from Tabu_functions import single_hospital_change
from Tabu_functions import external_patients_relocate
from Tabu_functions import external_patients_swap
from Tabu_functions import external_path_swap
from Tabu_functions import external_hospital_swap
from Tabu_functions import plotting
from Tabu_functions import node_to_edge
from Tabu_functions import has_green
from heuristic1 import partition
from heuristic1 import generateProb
from heuristic1 import get_part_h
from heuristic1 import heuristic
from heuristic1 import assign_in_partition

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


rnd=np.random
rnd.seed(10)
ng=10
nr=10
nh=4
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






#

def Simulated_Annealing(ng,nr,nh):
     prob=generateProb(ng,nr,nh)
     initial_solution=generate_initial_solution(prob)
#     first=copy.deepcopy(initial_solution)
     extract=extract_paths(prob.G,initial_solution)
     paths=extract[1]
     first_paths=copy.deepcopy(paths)
     current_solution=extract[0]
     current_cost=cost_solution(prob.G,current_solution)
     best_cost=current_cost
     best=current_solution
     hospital=[2,2,5,5,0,1,2,3,4,5,6]
     print("inital cost= ", best_cost)
     k=1
     T=10000
     for j in range(50000):
         number=rnd.randint(2,7)
         if j>10000:
             number=hospital[rnd.randint(len(hospital))]
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
     print("best cost= ",best_cost)
     extract=extract=extract_paths(prob.G,best)
     best=extract[0]
     best_path=extract[1]
#     print(paths)
#     print(first_paths)
     print(best_path)
     plotting(prob.G,best)
     
     return best
 
 
solution=Simulated_Annealing(100,25,4)

#


#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
