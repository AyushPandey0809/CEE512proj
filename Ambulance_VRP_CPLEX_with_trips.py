# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 08:11:13 2019

@author: Zeus
"""

# -*- coding: utf-8 -*-


import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from docplex.mp.model import Model
import math

rnd=np.random
rnd.seed(15)
##Time units in minutes and distance units in feet##

# ============================PARAMETERS========================
h_n=2 #number of hospitals    
r_n=10#number of red code patients
g_n=20 #number of green code patients
k_n=3 #number of ambulances
p_n=r_n+g_n #nnumber of all patients

w_g=1 #weight given to green patients
w_r=4 #weight given to red patients
d_i=5 #time to serve patient **currently constant but can be randomly  generated per patient by creating a new set d[i]
d_h=5 #time penalty for dropping patient at hospital *constant, but can be changed*
c_h=100 #capacity of hospitals: at least r_n+g_n **can be changed, currently it will always hav enouth capacity**
M=1000 #big number  *I believe this can affect computational time, it should be an upperbound for the arrival time of any patient *
# ============================SETS==============================
H=[i for i in range(0,h_n)] #set of Hospitals
H1=[i+h_n+r_n+g_n for i in H]
G=[i for i in range(h_n,h_n+g_n)] #set of green patients
R=[i for i in range(h_n+g_n,p_n+h_n)] #set of green patients       
   
P=R+G #all patients
PH=H+R+G #all patients and hospitals
PH1=R+G+H1
PHH1=H+R+G+H1
GH=G+H #green and hospitals
GH1=G+H1
A=[(i,j) for i in P for j in PH1 if i!=j] #set of Arcs 
for i in H:
    for j in P:
        A.append((i,j))
#for i in H1:
#    for j in H:
#        if i==j+len(PH):
#            A.append((i,j))


K=[i for i in range(1,k_n+1)] #set of ambulances
L=[i for i in PH] #set of trips
L1=[i for i in PH]
L1.append(len(PH))
Kh=[h for h in H] #set of ambulances initially located in H 
for h in H:
    Kh[h]=round(k_n/h_n) #locating equal amount of ambulances at each hospital
counter=0
while (sum(Kh)-k_n!=0):
    z=rnd.randint(0,len(H))#if number of ambulances is not a multiple of H, this will redistribute ambulances *could be changed easily*
    Kh[z]=max(Kh[1]+rnd.randint(-1,2),0)

loc_x=rnd.rand(len(PHH1))*5280*10
loc_y=rnd.rand(len(PHH1))*5280*10
for i in PHH1:
    if i>=len(PH):
        loc_x[i]=loc_x[i-len(PH)]
        loc_y[i]=loc_y[i-len(PH)]
    
c={(i,j):np.hypot(loc_x[i]-loc_x[j],loc_y[i]-loc_y[j]) for i, j in A} #cost between i,j
for i in H1:
    for j in H:
        c[i,j]=d_h

t={(i,j):c[i,j]/3080 for i,j in A} #time between i,j assuming 35mph speed=3080ft/min


# ========================INITIAL PLOT=======================================
plt.scatter(loc_x[0:h_n],loc_y[0:h_n], c='black',marker='s')
plt.scatter(loc_x[h_n:h_n+g_n],loc_y[h_n:h_n+g_n],c='g')#green patients
plt.scatter(loc_x[h_n+g_n:h_n+p_n],loc_y[h_n+g_n:h_n+p_n],c='r')
plt.axis('equal');

loc_x1=loc_x[:len(PH)]
loc_y1=loc_y[:len(PH)]
# ============================SUBSCRIPTS=========================================

X=[(k,l,i,j) for k in K for l in L1 for i,j in A] #Subscript for x_ij #1 iff ambulance serves patient i directly before patient j
BB=[(k,l,i) for k in K for l in L1 for i in PHH1] #subscript for b_i (time of patient visit)
U=[(k,l,i,h) for k in K for l in L for i in R for h in H1] #subscript for u_ih
Y=[(k,h,l,l+1) for k in K for l in L for h in H+H1]


# ===========================MODEL=============================================
mdl=Model('AmbulanceVRP',checker='off')
# ==========================DECISION VARIABLES=================================
x=mdl.binary_var_dict(X,name='x')
y=mdl.binary_var_dict(Y,name='y')
er=mdl.continuous_var(name='er',lb=0)
eg=mdl.continuous_var(name='eg',lb=0)
b=mdl.continuous_var_dict(BB,name='b',lb=0)


# ============================OBJECTIVE========================================
mdl.minimize(er+eg)
#mdl.minimize(mdl.sum(x[k,l,i,j]*t[i,j] for i,j in A for k in K for l in L))
# ============================CONSTRAINTS======================================


mdl.add_constraints(mdl.sum(x[k,0,h,j] for j in P for k in K)<=Kh[h] for h in H) #the amount of ambulances getting out of hospitals should not exceed the amount of ambulances available
mdl.add_constraints(mdl.sum(x[k,l,i,j] for j in PH1 if j!=i)==mdl.sum(x[k,l,j,i] for j in PH if j!=i) for i in P for l in L for k in K) # conservation of vehicles
mdl.add_constraints(mdl.sum(x[k,l,i,j] for i in PH if j!=i for k in K for l in L)==1 for j in P) #all patients need to be visited once only
mdl.add_constraints(mdl.sum(x[k,l,i,j] for j in P if j!=i)==0 for i in R for k in K for l in L) #all patients need to be visited once only
mdl.add_constraints(mdl.sum(x[k,l,j,h] for j in P)>=y[k,h,l,l+1] for h in H1 for k in K for l in L)
#mdl.add_constraints(mdl.sum(x[k,l,j,h+len(PH)] for j in P)>=x[k,l,h+len(PH),h] for h in H for k in K for l in L)
mdl.add_constraints(y[k,h+len(PH),l,l+1]==y[k,h,l,l+1] for k in K for l in L for h in H)
#mdl.add_constraints(x[k,l,h+len(PH),h]>=mdl.sum(x[k,l+1,h,j] for j in P) for k in K for l in L for h in H)
mdl.add_constraints(y[k,h,l,l+1]>=mdl.sum(x[k,l+1,h,j] for j in P) for h in H for k in K for l in L if l<len(L)-1)


mdl.add_constraints(mdl.sum(x[k,l,i,h] for i in R for k in K for l in L)<=c_h for h in H1) #the amount of people taken to hospitals should not exceed capacity of hospitals


mdl.add_indicator_constraints(mdl.indicator_constraint(x[k,l,i,j], b[k,l,i]+d_i+t[i,j]==b[k,l,j]) for l in L for k in K for i,j in A) #subtour elimination, keeping track of time for green patients

mdl.add_indicator_constraints(mdl.indicator_constraint(y[k,h,l,l+1], b[k,l,h+len(PH)]+d_h==b[k,l+1,h]) for h in H for l in L for k in K) #keeping track of time for red patients
#mdl.add_indicator_constraints(mdl.indicator_constraint(x[k,l,h+len(PH),h], b[k,l,h+len(PH)]+d_h==b[k,l+1,h]) for h in H for l in L for k in K) #keeping track of time for red patients


mdl.add_constraints(eg>=b[k,l,i] for k in K for l in L for i in G) #eg is the maximum serving time of all greens, so this takes care of the "max" function
mdl.add_constraints(er>=b[k,l,i]+t[i,h]+d_h for i in R for h in H1 for k in K for l in L) #er is the max serving time of red

#mdl.time_limit_parameter(20)
## =========================SOLVE====================================================
solution = mdl.solve(log_output=True)
objective=mdl.objective_value
print(objective)
print(solution)

## ========================PLOT SOLUTION==============================================
active_arcs= [(k,l,i,j) for k in K for l in L for i,j in A if x[k,l,i,j].solution_value>0.9]
plt.scatter(loc_x[0:h_n],loc_y[0:h_n], c='black',marker='s')
plt.scatter(loc_x[h_n:h_n+g_n],loc_y[h_n:h_n+g_n],c='g')#green patients
plt.scatter(loc_x[h_n+g_n:h_n+p_n],loc_y[h_n+g_n:h_n+p_n],c='r')


for k,l,i,j in active_arcs:
    plt.plot([loc_x[i], loc_x[j]], [loc_y[i],loc_y[j]],c='b', alpha=0.5)
    
for i in PH:
    plt.annotate((i),(loc_x[i]+200,loc_y[i]+200))
plt.axis('equal');











