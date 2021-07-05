from .loader import loader 
from .Makespan import Makespan
import numpy as np
import time



#Fonction qui calcule le coût de traitement d'une séquence donnée  
def cost(dataset, seq):
    bgTime=[]
    n,m=dataset.shape
    cost=0
    if(len(seq)<=n):
        #Le traitment de premier Job commence à t=0 dans la premiére machine.
        bgTime.append(0)
        #Calculer de démarrage du traitement du premier Job sur les autres machines.
        for j in range (m-1):
            bgTime.append(dataset.iloc[seq[0],j]+bgTime[j])

        #Pour les autres Jobs
        for i in range(len(seq)-1):
            #Le temps de démarrage du traitement du Job i sur première machine.
            bgTime[0]=bgTime[0]+dataset.iloc[seq[i],0]
            #Le temps de démarrage du traitement du Job i  sur les autres machines.
            for j in range(m-1):
                bgTime[j+1]=max(dataset.iloc[seq[i],j+1]+bgTime[j+1],dataset.iloc[seq[i+1],j]+bgTime[j])
        
        #cost contient le temps de fin de traitement du dernier Job de la séquence après lùexécution sur la dernière machine.
        cost = bgTime[m-1]+dataset.iloc[seq[len(seq)-1],m-1]
    
    return cost

#Palmer's Heuristic Algorithm.
def ph(dataset):
        n,m=dataset.shape
        #Function that helps the calculation of machines' weights.
        def palmer_f(x): return -(m - (2*x - 1))
        
        #Assigning specific weights to each machine and storing them in a list.
        weights = list(map(palmer_f, range(1, m+1)))
        ws = []
        #Evaluating the weight of each job by multiplying the weights with the processing times.
        for job_id in range(n):
            p_ij = sum([dataset.iloc[job_id,j]*weights[j]
                        for j in range(m)])
            ws.append((job_id, p_ij))
        #Sorting the jobs in the decreasing order of their weights.
        ws.sort(key=lambda x: x[1], reverse=True)
        #Formulating a sequence based on the sorting done up above.
        h_seq = [x[0] for x in ws]

        m_span = cost(dataset, h_seq)
      
        return h_seq,m_span

#dataPath="../data/tai20_5.txt"
#dataset53=loader(dataPath, machines_in_rows=True)

#start=time.time()
#optimalSeq,mkspan=ph(dataset53)
#end=time.time()


#print ('The optimal sequence is :',optimalSeq)
#print ("Makespan :",mkspan)
#print ('Execution time',end-start)
#Main Program   