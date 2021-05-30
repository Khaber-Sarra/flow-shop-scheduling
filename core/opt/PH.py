from loader import loader 
from Makespan import Makespan
import numpy as np
import time



#Function to calculate the cost of the given sequence.
def cost(dataset, seq):
    bgTime=[]
    n,m=dataset.shape
    cost=0
    if(len(seq)<=n):
        #The first job start at t=0 in the first machine
        bgTime.append(0)
        #Calculate the start time in the other machines
        for j in range (m-1):
            bgTime.append(dataset.iloc[seq[0],j]+bgTime[j])

        #For the other jobs
        for i in range(len(seq)-1):
            #The start time in the first machine
            bgTime[0]=bgTime[0]+dataset.iloc[seq[i],0]
            #The start time in the other machines
            for j in range(m-1):
                bgTime[j+1]=max(dataset.iloc[seq[i],j+1]+bgTime[j+1],dataset.iloc[seq[i+1],j]+bgTime[j])
        
        #cost contains the end time of the last job in the sequence after processing in the last machine
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
            p_ij = sum([dataset[j][job_id]*weights[j]
                        for j in range(m)])
            ws.append((job_id, p_ij))
        #Sorting the jobs in the decreasing order of their weights.
        ws.sort(key=lambda x: x[1], reverse=True)
        #Formulating a sequence based on the sorting done up above.
        h_seq = [x[0] for x in ws]
      
        return h_seq

#Main Program
print ("Exemple  5 Jobs / 3 Mahines")
dataPath="../data/data53.txt"
dataset53=loader(dataPath)

start=time.time()
optimalSeq=ph(dataset53)
end=time.time()

mkspan=cost(dataset53, optimalSeq)

print ('The optimal sequence is :',optimalSeq)
print ("Makespan :",mkspan)
print ('Execution time',end-start)