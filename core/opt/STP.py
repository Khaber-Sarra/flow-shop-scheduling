#coding=utf-8
import numpy as np
from loader import loader
from Makespan import Makespan
import time
import pandas as pd


def STP(data):
    Som=[]                      
    list=[]
    sol=[]
    Som=data.sum(axis=1).tolist()
    n,m=data.shape
   
    for i in range(n):
        list.append([Som[i],i])
    list=sorted(list,key=lambda x:x[0])
    for i in range(len(list)):
        sol.append(list[i][1])
    #retourner l'ordonnencement final
    return sol,Makespan(data,sol)

data = loader(f"./core/data/tai50_5.txt",machines_in_rows=True)  
start=time.time()
sol,makespan=STP(data)

#end=time.time()
#print("ordonnancement",sol)
#print("----------------------------------------")
#print("fin d'execution t=",makespan)
#print("----------------------------------------")
#print("le temps d'exec algorithme",end-start)

