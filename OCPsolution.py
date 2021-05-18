def destruction1(nSol, solution, alpha):
    nd=math.floor(nSol*alpha)
    rem=[]
    for i in range(nd):
        s=random.randint(0,nSol-1)
        nSol-=1
        rem.append(solution[s])
        solution.remove(solution[s])
    return [solution, nSol, rem]

def repair1(nCandidates, nSamples, solBinary, rem, cover):
    mod = Model("Camera_Placement")
    
    # Set of candidates
    set_C=range(nCandidates)
    
    # Decision variables
    X=mod.addVars(nCandidates,vtype=GRB.BINARY, name="Cameras")
    
    mod.update()
    
    # Constraints
    for j in range(nSamples):
        name= "Cnstr_"+str(j)
        ctr = LinExpr()
        for k in range(1,len(cover[j])):
            ctr.addTerms(1,X[cover[j][k]])
        mod.addConstr(ctr >= 1, name=name)
#        mod.addConstr(quicksum(p[i][j]*X[i] for i in range(nCandidates)) >= 1, name=name)
    
    for j in range(nCandidates):
        name= "Cnstr_"+str(nSamples+j)
        mod.addConstr(X[j] >= solBinary[j], name=name)
    
    ctr2 = LinExpr()
    for j in range(len(rem)):
        ctr2.addTerms(1,X[rem[j]])
    mod.addConstr(ctr2 <= len(rem)-1)
    
    # Objective function
    mod.setObjective(quicksum(X[i] for i in range(nCandidates)), GRB.MINIMIZE)
    mod.setParam(GRB.Param.OutputFlag, 0)
    
    mod.update()
    
    # Solve
    mod.optimize()
    
    nSol=mod.objVal
    #print(nSol)
    solution=[]
    for i in range(int(nCandidates)):
        if X[i].X >= 0.99:
            solution.append(i)
            
    return solution, nSol

def destruction2(nSol, solution, beta):
    nd=math.floor(nSol*beta)
    add=[]
    for i in range(nd):
        s=random.randint(0,nCandidates-1)
        while s in solution:
            s=random.randint(0,nCandidates-1)
        nSol+=1
        add.append(s)
        solution.append(s)
    return [solution, nSol, add]

def repair2(nCandidates, nSamples, solBinary, add, cover):
    mod = Model("Camera_Placement")
    
    # Set of candidates
    set_C=range(nCandidates)
    
    # Decision variables
    X=mod.addVars(nCandidates,vtype=GRB.BINARY, name="Cameras")
    
    mod.update()
    
    # Constraints
    for j in range(nSamples):
        name= "Cnstr_"+str(j)
        ctr = LinExpr()
        for k in range(1,len(cover[j])):
            ctr.addTerms(1,X[cover[j][k]])
        mod.addConstr(ctr >= 1, name=name)
#        mod.addConstr(quicksum(p[i][j]*X[i] for i in range(nCandidates)) >= 1, name=name)
    
    for j in range(nCandidates):
        name= "Cnstr_"+str(nSamples+j)
        mod.addConstr(X[j] <= solBinary[j], name=name)
    
    ctr2 = LinExpr()
    for j in range(len(add)):
        ctr2.addTerms(1,X[add[j]])
    mod.addConstr(ctr2 >= len(add)-1)
    
    # Objective function
    mod.setObjective(quicksum(X[i] for i in range(nCandidates)), GRB.MINIMIZE)
    mod.setParam(GRB.Param.OutputFlag, 0)
    
    mod.update()
    
    # Solve
    mod.optimize()
    
    nSol=mod.objVal
    #print(nSol)
    solution=[]
    for i in range(int(nCandidates)):
        if X[i].X >= 0.99:
            solution.append(i)
            
    return solution, nSol

def Best(P):
    nP=len(P)
    obj=[]
    for i in range(0,nP):
        obj.append(len(P[i][:]))
    sol=obj.index(min(obj))
    best=P[sol]
    return best


import time
import conda
import numpy as np
import random
import gurobipy as gp
from gurobipy import *
import math
import copy
from HybridGA import HybridGA

print("----------------------")
instances = [str(i).zfill(2) for i in range(1,2)]
for ins in instances:
    random.seed(5)
    # data = open("AC_"+ins+"_cover.txt", "r")
    data = open("C:/git/Instances/OCP/AC_"+ins+"_cover.txt", "r")
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
    for i in range(0,nSamples):
        size=len(cover[i])
        for j in range(1,size):
            candidates[cover[i][j]][0]+=1
            candidates[cover[i][j]].append(i)
#            p[cover[i][j]][i]=1
            
    del cand, nCand, size, data
    
    ct=time.time()

    coverOriginal=copy.deepcopy(cover)
    candidatesOriginal=copy.deepcopy(candidates)
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
    print("")
    
    alpha=0.4
    [solution2, nSol2, rem]= destruction1(nSol, solution, alpha)

    
    solBinary=np.zeros([nCandidates, 1])
    for i in range(nSol2):
        solBinary[solution2[i]]=1
    
    solution2, nSol2 = repair1(nCandidates, nSamples, solBinary, rem, coverOriginal)
    print(nSol2)
    print(solution2)
    print("")
    
    beta=0.4
    [solution3, nSol3, add]= destruction2(nSol2, solution2, beta)

    
    solBinary=np.zeros([nCandidates, 1])
    for i in range(int(nSol3)):
        solBinary[solution3[i]]=1

    solution3, nSol3 = repair2(nCandidates, nSamples, solBinary, add, coverOriginal)
    print(nSol3)
    print(solution3)
    print("")

    ct=time.time()-ct
    #print(ct)
    
    P=[solution, solution2, solution3]
    solution=Best(P)
    del candidates, cover, c, P, solution2, solution3
    solution=HybridGA(0.4, solution, 10, nCandidates, candidatesOriginal, nSamples, coverOriginal)