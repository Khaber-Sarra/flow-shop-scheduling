from loader import loader 
from Makespan import Makespan
import numpy as np
import time

optimalSeq=[] #Contains the optimal sequence after traitement
lb=0          #Lower Bound 

#Function to calculate the cost of the given sequence
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

#Function that returns the evaluation of a node
def eval(cost, dataset, rJobs):
    eval=cost 
    n,m=dataset.shape
    for j in rJobs:
        eval+=dataset.iloc[j][m-1]
    return eval

#Function that maps the tree of possible solutions using DFS method.
#returns the optimal one
def dfs(seq, rJobs, dataset):
    global lb
    global optimalSeq

    #Foreach remaining job in rJobs list
    for j in rJobs:
        seq1=[]
        rJobs1=[]
        seq1.extend(seq)
        rJobs1.extend(rJobs)
        #Add this job to the actual sequence and remove it from the remaining jobs list
        rJobs1.remove(j)
        seq1.append(j)

        #Calculate the cost of the new sequence 
        c=cost(dataset, seq1)  
        #if the mapping reached the lowest level in the branch
        if(len(rJobs1)==0):
            #if the cost of this branch is inferieur of the actual lower bound
            if(c<lb):
                #update the lower bound value
                lb=c 
                #update the optimal sequence
                optimalSeq=[]
                optimalSeq.extend(seq1) 
        else: #if there are other remaining jobs in the list
            #Calculate the evaluation of the actual node
            e=eval(c, dataset, rJobs1)
            #if the 'e' value is inferieur of the lower bound the mapping continues
            #else the branch is eliminated
            if(e<lb):
                dfs(seq1, rJobs1, dataset)
        
            
        


#Branch & bound function for FSP problem using DFS parcour 
def bb(dataset):
    global lb
    global optimalSeq
    seq=[]
    rJobs=[]
    n,m=dataset.shape

    #Generate a sequence to calculate the initial Lower Bound value
    for i in range(n):
        rJobs.append(i)
    lb=cost(dataset, rJobs)
    optimalSeq=rJobs
    #Call the DFS mapping function to get the optimal sequence
    dfs(seq, rJobs,dataset)
    return optimalSeq




print("First example")
dataPath="../data/bbdata.txt"
dataset=loader(dataPath)

start=time.time()
bb(dataset)
end=time.time()

print 'The optimal sequence is :',optimalSeq
print "Makespan :",lb
print 'Execution time',end-start 

print("\nSecond example")
dataPath="../data/data1.txt"
dataset=loader(dataPath)

start=time.time()
bb(dataset)
end=time.time()

print 'The optimal sequence is :',optimalSeq
print "Makespan :",lb
print 'Execution time',end-start  
