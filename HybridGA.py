import conda
import numpy as np
import random
import gurobipy as gp
from gurobipy import *
import math

def initialPopulation(nCandidates, candidates, nSamples, cover):
    samCovered=0
    solution=[]
    nSol=0
    coverOriginal=cover.copy()
    while samCovered==nSamples:
        can=random.randint(0,nCanditates)
        solution.append(can)
        nSol+=1
        samCovered+=candidates[can][0]
        i=1
        while i <= candidates[can][0]:
            j=1
            aux=candidates[can][i]
            while j <= cover[aux][0]:
                candidates[cover[aux][j]][0]-=1
                de=candidates[cover[aux][j]][1:].index(aux)
                candidates[cover[aux][j]][de+1]=[]
                candidates[cover[aux][j]].remove([])
                j+=1
            cover[aux][0]=nCandidates+1
    solBinary=np.zeros([nCandidates, 1])
    for i in range(nSol):
        solBinary[solution[i]]=1
        # cambiar reapir2 y quitar variable add
    solution, nSol = repair2(nCandidates, nSamples, solBinary, coverOriginal)
    return solution

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

def selection(P):
    x=random.randint(0,5)
    y=random.randint(0, 10)
    while y==x:
        y=random.randint(0,10)
    return x, y
    
def crossover(i, j, P):
    h=[]
    I=len(P[i])
    J=len(P[j])
    for k in range(I+1):
        h.append(P[i][k])
    for k in range(J+1):
        h.append(P[j][k])
        
    
def mutation(h, alpha, coverOriginal):
    nSol=len(h)
    [hM, nSol, rem]=destruction1(nSol, h, alpha)
    solBinary=np.zeros([nCandidates, 1])
    for i in range(int(nSol)):
        solBinary[hM[i]]=1
    hM, nSol = repair1(nCandidates, nSamples, solBinary, rem, coverOriginal)
    return hM
    
def update(H, P, candidates):
    nP=len(P)
    distances=np.zeros(nP,nP)
    for i in range(nP):
        for j in range(i,nP):
            distances[i][j]=dist(P[i],P[j])
            
    lamb = Lambda(P, candidates):
            
    mod = Model("Population_Update")
    b=Best(P)
    
    # Set of candidates
    set_C=range(nP)
    
    # Decision variables
    X=mod.addVars(nCandidates,vtype=GRB.BINARY, name="Cameras")
    
    mod.update()
    
    # Constraints
    for i in range(nP):
        for j in range(i+1,nP):
            name= "Cnstr_"+str(j)
            mod.addConstr(lamb[i] >= distance[i][j]-100*(2-X[i]-X[j]), name=name)
    
    mod.addConstr(sum(X[i])==len(P))
    mod.addConstr(X[b]==1)
    
    # Objective function
    mod.setObjective(quicksum(X[i] for i in range(nCandidates)), GRB.MINIMIZE)
    mod.setParam(GRB.Param.OutputFlag, 0)
    
    mod.update()
    
    # Solve
    mod.optimize()
    
def Lambda(P, candidates):
    nP=len(P)
    lamb=np.zeros(1,nP)
    for i in P:
        nS=len(P[i])
        for j in range(nS):
            lamb[i]+=candidates[0][j]
    return lamb
    
    
def Best(P):
    for i in P:
        obj=len(P[i])
    sol=obj.index(min(obj))

def HybridGA(alpha, sol0, n0, nCandidates, candidates, nSamples, cover, candidates):
    P=[]
    for i in range(n0):
        p=initialPopulation(nCandidates, candidates, nSamples, cover)
        P.append(p)
    P.append(sol0)
    H=[] #?
    while stop_criteria==False:
        nP=len(P)
        for s in range(nP)
            i, j = selection(P)
            h = crossover(i,j,P)
            hM = mutation(h, alpha, cover)
            H.append(h)
            H.append(hM)
        P = update(H, P, candidates)
    sol=Best(P)
    s=P[sol]
    return s