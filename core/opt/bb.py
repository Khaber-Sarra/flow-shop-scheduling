from .loader import loader 
from .Makespan import Makespan
import numpy as np
import time

optimalSeq=[] #La liste qui va contenir la séquence optimale à la fin du traitement.

ub=0    #Upper Bound (Borne supérieure) Aprés l'exécution de l'algorithme elle va contenir 
        #le temps de traitement globale de la séquence optimale dans toutes les machines.

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

#Fonction qui calcule l'évaluation d'un noeud donné 
def eval(cost, dataset, rJobs):
    eval=cost 
    n,m=dataset.shape
    for j in rJobs:
        eval+=dataset.iloc[j][m-1]
    return eval

#Fonction qui parcourt l'arbre des solutions possibles en utilisant la méthode DFS.
#elle retourne la séquence optimale
def dfs(seq, rJobs, dataset):
    global ub
    global optimalSeq
    
    #Pour chaque job restant dans la liste "rJobs".
    for j in rJobs:
        seq1=[]
        rJobs1=[]
        seq1.extend(seq)
        rJobs1.extend(rJobs)
        #Ajoutez ce job à la séquence actuelle et supprimez-la de la liste des job restants
        rJobs1.remove(j)
        seq1.append(j)

        #Calculer le coût de la nouvelle séquence 
        c=cost(dataset, seq1)  
        #Si le parcour atteint le niveau le plus bas de la branche
        if(len(rJobs1)==0):
            #Si le coût de la feuille de cette branche est inférieur à la borne supérieure actuelle
            if(c<ub):
                #Mettre à jour la borne limite supérieure
                ub=c 
                #Mettre à jour la séquence optimale
                optimalSeq=[]
                optimalSeq.extend(seq1) 
        else: #S'il reste d'autres job dans la liste des job restant
            #Calculer l'évaluation du nœud actuel
            e=eval(c, dataset, rJobs1)
            #Si la valeur 'e' est inférieure à la borne supérieure le parcour continue
            #Sinon la branche est éliminée
            if(e<ub):
                dfs(seq1, rJobs1, dataset)
        

#Johnson Algorthim pour le cas particulier avec uniquement deux machines 
def johnson_seq(data):
        global optimalSeq
        #La matrice de données ne doit avoir que deux machines
        nb_machines = len(data)
        nb_jobs = len(data[0])
        #Diviser l'ensemble des jobs en deux sous-ensembles
        machine_1_sequence = [j for j in range(nb_jobs) if data[0][j] <= data[1][j]]
        machine_2_sequence = [j for j in range(nb_jobs) if data[0][j] > data[1][j]]

        #Trier les deux sous-ensembles
        #Le premier est trié par ordre croissant
        machine_1_sequence.sort(key=lambda x: data[0][x])

        #Le second est trié par ordre décroissant
        machine_2_sequence.sort(key=lambda x: data[1][x], reverse=True)

        #Fusionner les deux sous-ensembles en un seul ensemble qui représente la séquence optimale
        optimalSeq = machine_1_sequence + machine_2_sequence

#Fonction "Branch and Bound" qui retourne la séquence optimale pour le problème FSP. 
def bb(dataset):
    global ub
    global optimalSeq
    seq=[]           
    rJobs=[]
    n,m=dataset.shape
    if m==2 : #Traiter le cas particulier ou on a seulement 2 machines en utilisant Johnson Méthod
        johnson_seq(dataset)
        ub=cost(dataset, optimalSeq)
    else:#Le cas général
        #Générer une séquence pour calculer la valeur initiale de la borne supérieure
        for i in range(n):
            rJobs.append(i)
        ub=cost(dataset, rJobs)
        optimalSeq=rJobs
        #Appelez la fonction de prcour DFS pour obtenir la séquence optimale
        dfs(seq, rJobs,dataset)
    return optimalSeq




#print ("First example  6 Jobs / 5 Mahines")
#dataPath="../data/data6-5.txt"
#dataset65=loader(dataPath)
#
#start=time.time()
#bb(dataset65)
#end=time.time()
#
#print ('The optimal sequence is :',optimalSeq)
#print ("Makespan :",ub)
#print ('Execution time',end-start)
#
#print ("\nSecond example  8 Jobs / 5 machines")
#dataPath="../data/data8-5.txt"
#dataset85=loader(dataPath)
#
#start=time.time()
#bb(dataset85)
#end=time.time()
#
#print ('The optimal sequence is :',optimalSeq)
#print ("Makespan :",ub)
#print ('Execution time',end-start) 
#
#print ("Third example  500 Jobs / 2 machines")
#dataPath="../data/data500-2.txt"
#dataset=loader(dataPath)
#
#start=time.time()
#bb(dataset)
#end=time.time()
#
#print ('The optimal sequence is :',optimalSeq)
#print ("Makespan :",ub)
#print ('Execution time',end-start)  