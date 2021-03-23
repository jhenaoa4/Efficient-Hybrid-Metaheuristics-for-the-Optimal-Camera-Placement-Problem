def destruction1(nSol, solution, alpha):
    nd=math.floor(nSol*alpha)
    rem=[]
    for i in range(nd):
        s=random.randint(0,nSol-1)
        nSol-=1
        rem.append(solution[s])
        solution.remove(solution[s])
    return [solution, nSol, rem]

def repair1(nCandidates, p, nSamples, solBinary, rem, cover):
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

def repair2(nCandidates, p, nSamples, solBinary, add, cover):
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
    mod.addConstr(ctr2 >= 1)
    
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

import time
import conda
import numpy as np
import random
import gurobipy as gp
from gurobipy import *
import math

print("----------------------")
instances = [str(i).zfill(2) for i in range(1,5)]
for ins in instances:
    print("--- Instance ", ins, " ---")
    random.seed(5)
#    data = open("AC_"+ins+"_cover.txt", "r")
    data = open("C:\Git\Instances\OCP\AC_"+ins+"_cover.txt", "r")
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
    
    bestf=nCandidates
            
    candidates=[[el * 0] for el in range(0,nCandidates)]
#    p=np.zeros([nCandidates, nSamples])
    for i in range(0,nSamples):
        size=len(cover[i])
        for j in range(1,size):
            candidates[cover[i][j]][0]+=1
            candidates[cover[i][j]].append(i)
#            p[cover[i][j]][i]=1
            
    del cand, nCand, size, data
    
    ct=time.time()

    coverOriginal=cover.copy()
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
    if nSol < bestf:
        bestf=nSol
        print(bestf)
#    print("First solution")
#    print(nSol, solution)
#    print("")
    
    it=0
    while it<20:
        it+=1
    
        alpha=0.4
        [solution, nSol, rem]= destruction1(nSol, solution, alpha)
#        print("Destruction: Removing candidates")
#        print(nSol)
#        print(solution)
#        print(rem)
#        print("")
    
        
        solBinary=np.zeros([nCandidates, 1])
        for i in range(int(nSol)):
            solBinary[solution[i]]=1
        
        p=[]
        solution, nSol = repair1(nCandidates, p, nSamples, solBinary, rem, coverOriginal)
        if nSol < bestf:
            bestf=nSol
            print(bestf)
#        print("Reparation 1 with Gurobi")
#        print(nSol, solution)
#        print("")
        
        beta=10
        [solution, nSol, add]= destruction2(nSol, solution, beta)
#        print("Destruction: Adding candidates")
#        print(nSol)
#        print(solution)
#        print(add)
#        print("")
    
        
        solBinary=np.zeros([int(nCandidates), 1])
        for i in range(int(nSol)):
            solBinary[solution[i]]=1
    
        solution, nSol = repair2(nCandidates, p, nSamples, solBinary, add, coverOriginal)
        if nSol < bestf:
            bestf=nSol
            print(bestf)
#        print("Reparation 2 with Gurobi")
#        print(nSol, solution)
#        print("")

    print("Time")
    ct=time.time()-ct
    print(ct)