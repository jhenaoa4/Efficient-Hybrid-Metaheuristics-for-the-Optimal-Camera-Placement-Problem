import conda
import numpy as np
import random
instances = [str(i).zfill(2) for i in range(1,2)]
for ins in instances:
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
    for i in range(0,nSamples):
        size=len(cover[i])
        for j in range(1,size):
            candidates[cover[i][j]][0]+=1
            candidates[cover[i][j]].append(i)
            
    del cand, nCand, size, data
    
    coverOriginal=cover
    c=[item[0] for item in cover]
    nSol=0
    samplesCovered=0
    solution=[]
    k=1
    while samplesCovered < nSamples:
        print(samplesCovered)
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
            # i+=1
        k+=1