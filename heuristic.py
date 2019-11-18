#!/usr/bin/env python
# coding: utf-8

# In[38]:


from collections import defaultdict
import numpy as np
import math
import matplotlib.pyplot as plt
rnd = np.random
rnd.seed(4)

class node:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        
class edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.cost = ((start.x-end.x)**2+(start.y-end.y)**2)**(1/2)
        
class sol:
    def __init__(self, nodes, edges):
        self.nodes = nodes      #array of nodes in solution
        self.edges = edges      #array of edges in solution
        self.total_cost = get_total_cost(self)
        
    def get_total_cost(self):
        total = 0
        for i in self.edges:
            total = total + i.cost
        return total
    
class partition:
    def __init__(self, G, E):
        self.G = G
        self.E = E


# In[39]:


def generateProb(ng, nr, nh):
    G = []
    for i in range(nh):
        G.append(node(rnd.randint(20), rnd.randint(20), 1))
    for i in range(ng):
        G.append(node(rnd.randint(20), rnd.randint(20), 2))
    for i in range(nr):
        G.append(node(rnd.randint(20), rnd.randint(20), 3))
        
    E = [edge(G[i], G[j]) for i in range(ng + nr + nh) for j in range(ng + nr + nh) if i!=j]
    
    prob = partition(G, E)
    
    return prob


# In[72]:


def get_part_h(G, E):
    partitions = []
    red = [x for x in G if x.type == 3]
    green = [x for x in G if x.type == 2]
    hosp = [x for x in G if x.type == 1]
    part = []
    for i in hosp:
        part.append(partition([i], []))
    maxr = math.ceil(len(red)/len(hosp))
    maxg = math.ceil(len(green)/len(hosp))
    for i in red:
        d = [x.cost for x in E if x.start==i if x.end.type==1]
        while True:
            idx = np.argmin(d)
            if (len(part[idx].G)) > maxr:
                d[idx] = math.inf
            else:
                part[idx].G.append(i)
                break
    for i in green:
        d = [x.cost for x in E if x.start==i if x.end.type==1]
        while True:
            idx = np.argmin(d)
            if (len(part[idx].G)) > maxr + maxg:
                d[idx] = math.inf
            else:
                part[idx].G.append(i)
                break
    for i in part:
        i.E = [edge(k, l) for k in i.G for l in i.G if k!=l]
    return part


# In[41]:


def heuristic(G, E):
    red = [x for x in G if x.type == 3]
    green = [x for x in G if x.type == 2]
    hosp = [x for x in G if x.type == 1]
    partitions = get_part_h(G, E)
    for i in partitions:
        
    return partitions


# In[73]:


prob = generateProb(6, 2, 2)
a = get_part_h(prob.G, prob.E)


# In[74]:


print(a)


# In[75]:


for i in a:
    print(i.G, i.E)


# In[59]:


a = np.empty(2, dtype = partition)
a[0] = generateProb(2, 2 , 2)
a[1] = generateProb(3, 3 , 3)


# In[60]:


a


# In[66]:





# In[ ]:




