def destruction1(nSol, solution, alpha):
    nd=math.floor(nSol*alpha)
    for i in range(1,nd):
        s=random.randint(0,nsol)
        nsol-=1
        solution.remove(solution[s])
    return [solution, nSol]

def repair1(nCandidates, p, nSamples, solBinary):
    mod = Model("Camera_Placement")
    
    # Set of candidates
    set_C=range(nCandidates)
    
    # Decision variables
    X=mod.addVars(nCandidates,vtype=GRB.BINARY, name="Cameras")
    
    mod.update()
    
    # Constraints
    for j in range(nSamples):
        name= "Cnstr_"+str(j)
        mod.addConstr(quicksum(p[i][j]*X[i] for i in range(nCandidates)) >= 1, name=name)
    
    for j in range(nCandidates):
        name= "Cnstr_"+str(nSamples+j)
        mod.addConstr(X[j] >= solBinary[j], name=name)
    
    # Objective function
    mod.setObjective(quicksum(X[i] for i in range(nCandidates)), GRB.MINIMIZE)
    
    mod.update()
    
    # Solve
    mod.optimize()
    
    nSol=mod.objVal
    print(nSol)
    solution=[]
    for i in range(nSol):
        if X[i].X == 1:
            solution.append(i)
            
    return solution

import conda
import numpy as np
import random
import gurobipy as gp
from gurobipy import *
import math

instances = [str(i).zfill(2) for i in range(1,2)]
for ins in instances:
    random.seed(5)
    data = open("AC_"+ins+"_cover.txt", "r")
    nSC=data.readline().split()
    nSamples=int(nSC[0])
    nCandidates=int(nSC[1])
    cover=[]
    for i in range(0,nSamples):
        ind=int(data.readline())
        nCand=int(data.readline())
        cand=data.readline().split()
        cover.append([])
        cover[ind].append(nCand)
        for i in cand:
            cover[ind].append(int(i))
            
    candidates=[[el * 0] for el in range(0,nCandidates)]
    # p=np.zeros([nCandidates, nSamples])
    for i in range(0,nSamples):
        size=len(cover[i])
        for j in range(1,size):
            candidates[cover[i][j]][0]+=1
            candidates[cover[i][j]].append(i)
            # p[cover[i][j]][i]=1
            
    del cand, nCand, size, data
    
    coverOriginal=cover
    c=[item[0] for item in cover]
    nSol=0
    samplesCovered=0
    solution=[]
    k=1
    while samplesCovered < nSamples:
        minim=c.index(min(c))
        maxAll=0
        for i in range(1,cover[minim][0]+1):
            if candidates[cover[minim][i]][0]>maxAll:
                maxAll=candidates[cover[minim][i]][0]
                sel=cover[minim][i]
        maxAll=sel
        solution.append(maxAll)
        nSol+=1
        samplesCovered+=candidates[maxAll][0]
        
        i=1
        while i <= candidates[maxAll][0]:
            j=1
            aux=candidates[maxAll][i]
            while j <= cover[aux][0]:
                candidates[cover[aux][j]][0]-=1
                de=candidates[cover[aux][j]][1:].index(aux)
                candidates[cover[aux][j]][de+1]=[]
                candidates[cover[aux][j]].remove([])
                j+=1
            cover[aux][0]=nCandidates+1
            c[aux]=nCandidates+1
    print(nSol)
    print(solution)
    
    alpha=0.2
    [solution, nSol]= destruction1(nSol, solution, alpha)
    
    solBinary=np.zeros([nCandidates, 1])
    for i in range(nSol):
        solBinary[solution[i]]=1
    
    solution=repair1(nCandidates, p, nSamples, solBinary)
    print(solution)

  

        