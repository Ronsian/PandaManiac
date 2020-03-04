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
import urllib.request

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

file="27.10.2.json"

k=file.split(".")

with open(file) as f:
  g = json.load(f)

G=nx.Graph(g)
n1=int(k[1])   #seeds
n2=int(k[0])  #teams
n=G.number_of_nodes() #nodes
ranked=degrank(G,n) #list of nodes in order of degree

with urllib.request.urlopen("http://35.167.100.168:3000/download/"+file[0:-5]+"-socialscinerds.json") as url:
    data = json.loads(url.read().decode())

out=[]
ite={}
val=[]
for i in range(50):
    for key in data:
        if key=="socialscinerds":
            seeds=lol(G,n1,2,ranked)
            ite[key]=seeds
        else:
            ite[key]=data[key][i]
            
    out.append(sim.run(g,ite))

    
for i in out:
    val.append(i["socialscinerds"]/n)
print(np.mean(val))
