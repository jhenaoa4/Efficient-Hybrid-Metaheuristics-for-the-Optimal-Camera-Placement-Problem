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

def selection(P):
    
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
    
def acceptance(h, hM, P):
    
def Best(P):
    for i in P:
        obj=len(P[i])
    sol=obj.index(min(obj))

def HybridGA(alpha, sol0, n0, nCandidates, candidates, nSamples, cover):
    P=[]
    for i in range(n0):
        p=initialPopulation(nCandidates, candidates, nSamples, cover)
        P.append(p)
    P.append(sol0)
    while stop_criteria==False:
        #esto para cuales soluciones
        i, j = selection(P)
        h = crossover(i,j,P)
        hM = mutation(h, alpha, cover)
        P = acceptance(h, hM, P)
    sol=Best(P)
    s=P[sol]
    return s