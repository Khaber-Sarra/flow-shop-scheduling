#coding=utf-8
import numpy
from loader import loader
from Makespan import Makespan
import time
import threading

Som=[]                      
Inf=[]
Sup=[]

def sortInf(data):
    #trier la liste Inf selon l'ordre croissant de P1
    Inf=sorted(data,key=lambda x:x[0])

def sortSup(data):
     #trier la liste Sup selon l'ordre décroissant de Pm
    Sup=sorted(data,key=lambda x:x[0], reverse=True)

'''
cette fonction prend en parametre la matrice des temps d'exec des jobs sur les machines
et retourne l'ordonnancement des jobs et le temps de fin d'exec
'''

def Chen(dataset):

   
    #lire les donnees depuis le nom de fichier en entrée "Dataset"
    data = loader(dataset,machines_in_rows=False)
    print(data)
    print("----------------------------------------")
    #calculer la somme des temps d'execution de chaque job sur toutes les machines dans Som
    Som=data.sum(axis=1).tolist()
    ##print(Som)
    #recuperer le job avec le temps d'exec max  
    maxIndex=Som.index(max(Som)) # C
    ##print("maxIndex",maxIndex)
    n,m=data.shape
    #creer deux liste : Inf contenant les jobs avec P1<=Pm  et Sup contenant les jobs avec P1>Pm
    for i in range(n):
        if (i != maxIndex):
            if (data.iloc[i,0]<=data.iloc[i,m-1]):
                Inf.append([data.iloc[i,0],i])
            else :
                Sup.append([data.iloc[i,m-1],i])

    # creer deux threads pour la parallelisation du tri des sequences Inf et Sup
    t1 = threading.Thread(target=sortInf,args=(Inf,))
    t2 = threading.Thread(target=sortSup,args=(Sup,))
  
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
  
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
    ##print("La premiere sequence",Inf)

    ##print("La deuxieme sequence",Sup)
    sol =[]
    #concatener les liste : Inf, Max, Sup dans la solution finale
    for i in range(len(Inf)):
        sol.append(Inf[i][1])
    sol.append(maxIndex)
    for i in range(len(Sup)):
        sol.append(Sup[i][1])
   
    #retourner l'ordonnencement final
    return sol,Makespan(data,sol)
    
start=time.time()
sol,makespan=Chen("../data/data.txt")
end=time.time()
print("ordonnancement",sol)
print("----------------------------------------")
print("fin d'execution t=",makespan)
print("----------------------------------------")
print("le temps d'exec algorithme",end-start)

