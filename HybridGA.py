import conda
import numpy as np
import random
import gurobipy as gp
from gurobipy import *
import math
import copy
import pandas as pd

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

def destruction2(nSol, solution, beta, nCandidates):
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

## ********************************************************
# Al menos un candidato de cada padre debe ser seleccionado
## ********************************************************

#    ctr2 = LinExpr()
#    for j in range(len(add)):
#        ctr2.addTerms(1,X[add[j]])
#    mod.addConstr(ctr2 >= len(add)-1)
    
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

def repair3(nCandidates, nSamples, solBinary, cover):
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

def initialPopulation(nCandidates, candidates1, nSamples, cover1, coverOriginal):
    samCovered=0
    solution1=[]
    nSol=0
    while samCovered<nSamples:
        can=random.randint(0,nCandidates-1)
        solution1.append(can)
        nSol+=1
        samCovered+=candidates1[can][0]
        i=1
        while i <= candidates1[can][0]:
            j=1
            aux=candidates1[can][i]
            while j <= cover1[aux][0]:
                candidates1[cover1[aux][j]][0]-=1
                de=candidates1[cover1[aux][j]][1:].index(aux)
                candidates1[cover1[aux][j]][de+1]=[]
                candidates1[cover1[aux][j]].remove([])
                j+=1
            cover1[aux][0]=nCandidates+1
    solBinary=np.zeros([nCandidates, 1])
    for i in range(nSol):
        solBinary[solution1[i]]=1
    #print(nSol)
    solution1, nSol = repair3(nCandidates, nSamples, solBinary, coverOriginal)
    del cover1, candidates1
    return solution1


def dist(p1,p2):
    nP1=len(p1)
    nP2=len(p2)
    t=0
    for i in p1:
        for j in p2:
            if i==j:
                t+=1
    d=nP1+nP2-2*t
    return d

def selection():
    x=random.randint(0, 5)
    y=random.randint(0, 10)
    while y==x:
        y=random.randint(0,10)
    return x, y
    
def crossover(i, j, P):
    h=[]
    I=len(P[i])
    J=len(P[j])
    for k in range(I):
        h.append(P[i][k])
    for k in range(J):
        h.append(P[j][k])
    return h
        
    
def mutation(h, alpha, coverOriginal, nCandidates, nSamples):
    nSol=len(h)
    [hM, nSol, add]=destruction2(nSol, h, alpha, nCandidates)
    solBinary=np.zeros([nCandidates, 1])
    for i in range(int(nSol)):
        solBinary[hM[i]]=1
    hM, nSol = repair2(nCandidates, nSamples, solBinary, add, coverOriginal)
    return hM
    
def update(H, P):
    P=[P, H]
    nP=len(P)
    # distances=np.zeros(nP,nP)
    distances=[]
    for i in range(nP-1):
        distances.append([])
        for j in range(i+1,nP):
            # distances[i][j]=dist(P[i],P[j])
            distances[i].append(dist(P[i],P[j]))
    

    mod = Model("Population_Update")
    b=Best(P)
    
    # Set of individuals
    set_C=range(nP)
    
    # Decision variables
    X=mod.addVars(nP,vtype=GRB.BINARY, name="Population")
    lamb=mod.addVar(lb=0.0, ub=float('inf'),vtype=GRB.CONTINUOUS, name="lambda")
    
    mod.update()
    
    # Constraints
    for i in range(nP-1):
        for j in range(nP-i-1):
            name= "Cnstr_"+str(j)
            mod.addConstr(lamb >= distances[i][j]-100*(2-X[i]-X[j]), name=name)
    
    mod.addConstr(sum(X)==len(P))
    mod.addConstr(X[b]==1)
    
    # Objective function
    mod.setObjective(lamb, GRB.MINIMIZE)
    mod.setParam(GRB.Param.OutputFlag, 1)
    
    mod.update()
    
    # Solve
    mod.optimize()
    
    nP=sum(X)
    Pnew=[]
    for i in range(nP):
        if X[i].X >= 0.99:
            Pnew.append(P[i])
    
    return Pnew
      
def coeficient(P, candidates):
    nP=len(P)
    coef=[[]]
    for i in range(0,nP):
        nS=len(P[i])
        coef[0].append(0)
        for j in range(nS):
            coef[0][i]+=candidates[0][j]
    return coef
    
    
def Best(P):
    nP=len(P)
    obj=[]
    for i in range(0,nP):
        obj.append(len(P[i][:]))
    sol=obj.index(min(obj))
    return sol

def HybridGA(alpha, sol0, n0, nCandidates, candidates, nSamples, cover):
    P=[]
    coverOriginal=copy.deepcopy(cover)
    candidatesOriginal=copy.deepcopy(candidates)
    for i in range(n0-1):
        candidates=copy.deepcopy(candidatesOriginal)
        cover=copy.deepcopy(coverOriginal)
        p=initialPopulation(nCandidates, candidates, nSamples, cover, coverOriginal)
        P.append(p)
    P.append(sol0)
    H=[]
    # stop_criteria=True
    # while stop_criteria==True:
    for it in range(100):
        nP=len(P)
        for s in range(nP):
            #print(s)
            Psort = coeficient(P, candidatesOriginal)
            Psort.append(P)
            Psort=pd.DataFrame(Psort)
            Psort.sort_values(by=0, axis=1)
            Psort=Psort.values.tolist()
            P=Psort[:][1]
            i, j = selection()
            h = crossover(i,j,P)
            hM = mutation(h, alpha, coverOriginal, nCandidates, nSamples)
            H.append(h)
            H.append(hM)
        P = update(H, P)
    sol=Best(P)
    s=P[sol]
    return s, P