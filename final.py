#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 12:50:41 2020

@author: amit
"""

import numpy as np
import networkx as nx
import json
import sim
import operator
import itertools 
from collections import Counter 

def findsubsets(s, n):  #generate all subsets of size n from list s
    return list(itertools.combinations(s, n))
    
def degrank(G,n1): #generates top n1 nodes according to degree
	draw = sorted(G.degree, key=lambda x: x[1], reverse=True)
	draw = [x[0] for x in draw]	
	return list(draw[:n1])

def opt(G,g,n1,ranked, k): #finds k-best response to highest degree strategy for 2 teams
    s1=ranked[:n1] #opponent strategy
    p1=ranked[:(n1-k)] #part 1 of strategy
    source=ranked[(n1-k):(n1+10)] #source for part 2 of strategy
    val={}
    ch={}
    it=findsubsets(source, k)
    for i in range(len(it)):
        z=list(it[i])
        s2=p1+z
        check={"opp":s1, "me":s2}
        x=sim.run(g, check)
        val[i]=x["me"]
        ch[i]=s2
    ind = Counter(val) 
    high = ind.most_common(2*k)
    fin=[]
    for i in high:
        fin.append(ch[i[0]])
    #a1=max(val.items(), key=operator.itemgetter(1))[0]
    #return ch[a1]
    return fin

def deg(G,n1,ranked,s,e): #choose seeds with moderately high degree uniformly
    n=G.number_of_nodes() #nodes
    start=s*n1
    end=e*n1
    source=ranked[start:end]
    draw=np.random.choice(source, n1, replace=False)
    return list(draw)

file="6.20.1.json"

k=file.split(".")

with open(file) as f:
  g = json.load(f)

G=nx.Graph(g)
n1=int(k[1])   #seeds
n2=int(k[0])  #teams
n=G.number_of_nodes() #nodes
ranked=degrank(G,n) #list of nodes in order of degree
out=[]
if n2==27:
    for i in range(50):
        s=4
        e=14
        seeds=deg(G,n1,ranked, s, e)
        out.append(seeds)
if n2==13:
    for i in range(50):
        s=2
        e=8
        seeds=deg(G,n1,ranked, s, e)
        out.append(seeds)
if n2==6:
    for i in range(50):
        s=1
        e=5
        seeds=deg(G,n1,ranked, s, e)
        out.append(seeds)
if n2==8:
    for i in range(50):
        s=1
        e=8
        seeds=deg(G,n1,ranked, s, e)
        out.append(seeds)
if n2==4:
    for i in range(50):
        s=1
        e=4
        seeds=deg(G,n1,ranked, s, e)
        out.append(seeds)
if n2==2:
    cutoff=5
    fins=[]
    for i in range(cutoff):
        fins.append(opt(G,g,n1,ranked, i+1))
    anss = [item for sublist in fins for item in sublist]
    t=len(anss)
    for i in range(50):
        m=i%t
        s=anss[m]
        out.append(s)

out = [item for sublist in out for item in sublist]

with open('output.txt', 'w') as f:
    for item in out:
        f.write("%s\n" % item)

