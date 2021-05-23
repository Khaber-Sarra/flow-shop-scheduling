from loader import loader 
from Makespan import Makespan
import numpy as np
import time

optimalSeq=[] #Contains the optimal sequence after traitement
ub=0          #Upper Bound, After excuting the algorithm it will contain the makespan of the optimal sequence 

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
    global ub
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
            #if the cost of this branch is inferieur of the actual upper bound
            if(c<ub):
                #update the upper bound value
                ub=c 
                #update the optimal sequence
                optimalSeq=[]
                optimalSeq.extend(seq1) 
        else: #if there are other remaining jobs in the list
            #Calculate the evaluation of the actual node
            e=eval(c, dataset, rJobs1)
            #if the 'e' value is inferieur of the upper bound the mapping continues
            #else the branch is eliminated
            if(e<ub):
                dfs(seq1, rJobs1, dataset)
        

#Johnson Algorthim for the particular case with only tow machines  
def johnson_seq(data):
        global optimalSeq
        #data matrix must have only two machines
        nb_machines = len(data)
        nb_jobs = len(data[0])
        #divide the set of jobs into two subsets
        machine_1_sequence = [j for j in range(nb_jobs) if data[0][j] <= data[1][j]]
        machine_2_sequence = [j for j in range(nb_jobs) if data[0][j] > data[1][j]]

        #sort the two subsets 
        #The first one is sorted in ascending order
        machine_1_sequence.sort(key=lambda x: data[0][x])

        #THe second one is sorted descending order
        machine_2_sequence.sort(key=lambda x: data[1][x], reverse=True)

        #Merge the two subsets into one set which represente the optimale sequence
        optimalSeq = machine_1_sequence + machine_2_sequence

#Branch & bound function for FSP problem using DFS parcour 
def bb(dataset):
    global ub
    global optimalSeq
    seq=[]
    rJobs=[]
    n,m=dataset.shape
    if m==2 :
        johnson_seq(dataset)
        ub=cost(dataset, optimalSeq)
    else:
        #Generate a sequence to calculate the initial Upper Bound value
        for i in range(n):
            rJobs.append(i)
        ub=cost(dataset, rJobs)
        optimalSeq=rJobs
        #Call the DFS mapping function to get the optimal sequence
        dfs(seq, rJobs,dataset)
    return optimalSeq




print ("First example  6 Jobs / 5 Mahines")
dataPath="../data/data6-5.txt"
dataset65=loader(dataPath)

start=time.time()
bb(dataset65)
end=time.time()

print ('The optimal sequence is :',optimalSeq)
print ("Makespan :",ub)
print ('Execution time',end-start)

print ("\nSecond example  8 Jobs / 5 machines")
dataPath="../data/data8-5.txt"
dataset85=loader(dataPath)

start=time.time()
bb(dataset85)
end=time.time()

print ('The optimal sequence is :',optimalSeq)
print ("Makespan :",ub)
print ('Execution time',end-start) 

print ("Third example  500 Jobs / 2 machines")
dataPath="../data/data500-2.txt"
dataset=loader(dataPath)

start=time.time()
bb(dataset)
end=time.time()

print ('The optimal sequence is :',optimalSeq)
print ("Makespan :",ub)
print ('Execution time',end-start)  