from loader import loader
import numpy as np
import math
import time
import random
import itertools
from Makespan import Makespan





#initialisation de la population de Npop individus parmi n jobs
def initialization(Npop,n):
    pop = []
    for i in range(Npop):
        p = list(np.random.permutation(n))
        while p in pop:
            p = list(np.random.permutation(n))
        pop.append(p)
    return pop

#############################################################################

#calculer le makespan d'une solution sol
def calculateObj(data,sol):      
    return Makespan(data,sol)


#############################################################################


#selection des individus a reproduire et qui participent a la construction d'une nouvelle population
def selection(pop,data):
    popObj = []
    for i in range(len(pop)):
        popObj.append([calculateObj(data,pop[i]), i])
    
    popObj.sort()
    
    distr = []
    distrInd = []
    
    for i in range(len(pop)):
        distrInd.append(popObj[i][1])
        prob = (2*(i+1)) / (len(pop) * (len(pop)+1))
        distr.append(prob)
    
    parents = []
    for i in range(len(pop)):
        parents.append(list(np.random.choice(distrInd, 2, p=distr)))
    
    return parents


#############################################################################

#creer de nouveaux individus en combinant les caracteristiques des differentes solutions (parents)
#Npop * Pc(proba de croisement) individus subissent un croisement
def crossover(parents,n):
    pos = list(np.random.permutation(np.arange(n-1)+1)[:2])
    
    if pos[0] > pos[1]:
        t = pos[0]
        pos[0] = pos[1]
        pos[1] = t
    
    child = list(parents[0])
    
    for i in range(pos[0], pos[1]):
        child[i] = -1
    
    p = -1
    for i in range(pos[0], pos[1]):
        while True:
            p = p + 1
            if parents[1][p] not in child:
                child[i] = parents[1][p]
                break
    
    return child


#############################################################################


#creation de nouveaux individus par mutation d'une proba Pm
def mutation(sol,n):
    pos = list(np.random.permutation(np.arange(n))[:2])
    
    if pos[0] > pos[1]:
        t = pos[0]
        pos[0] = pos[1]
        pos[1] = t
    
    remJob = sol[pos[1]]
    
    for i in range(pos[1], pos[0], -1):
        sol[i] = sol[i-1]
        
    sol[pos[0]] = remJob
    
    return sol

#############################################################################

#mise a jour de la population par un remplacement d'un enfant par le meilleur parent 
#afin de garder la taille de la population constante
def elitistUpdate(oldPop, newPop,data):
    bestSolInd = 0
    bestSol = calculateObj(data,oldPop[0])
    
    for i in range(1, len(oldPop)):
        tempObj = calculateObj(data,oldPop[i])
        if tempObj < bestSol:
            bestSol = tempObj
            bestSolInd = i
            
    rndInd = random.randint(0,len(newPop)-1)
    
    newPop[rndInd] = oldPop[bestSolInd]
    
    return newPop

#############################################################################

#retourner la meilleur solution de la population, la valeur de la fct objective 
def findBestSolution(pop,data):
    bestObj = calculateObj(data,pop[0])
    bestInd = 0
    for i in range(1, len(pop)):
        tObj = calculateObj(data,pop[i])
        if tObj < bestObj:
            bestObj = tObj
            bestInd = i
            
    return bestInd, bestObj

#############################################################################

'''
cette fonction prend en parametre la matrice des temps d'exec des jobs sur les machines
et retourne l'ordonnancement des jobs et le temps de fin d'exec
'''

#main
def AG(dataset):

   
    #lire les donnees depuis le nom de fichier en entrée "Dataset"
    data = loader(dataset,machines_in_rows=False)
    cost=data.to_numpy()
    n,m=cost.shape
    print(data)
    
    print(n,m)
    # Nombre d'indiv dans la population
    Npop = 3
    # Probabilité de croisement
    Pc = 1.0
    # Probabilité de mutation
    Pm = 1.0
    # critere d'arret
    stopGeneration = 100

    # temps debut exec
    t1 = time.time()

    # Creation de la population initiale
    population = initialization(Npop,n)

    
    for i in range(stopGeneration):
        # Selection des parents
        parents = selection(population,data)
        childs = []
        
        # appliquer le croisement
        for p in parents:
            r = random.random()
            if r < Pc:
                childs.append(crossover([population[p[0]], population[p[1]]],n))
            else:
                if r < 0.5:
                    childs.append(population[p[0]])
                else:
                    childs.append(population[p[1]])
        
        # Appliquer la mutation 
        for c in childs:
            r = random.random()
            if r < Pm:
                c = mutation(c,n)

        # Mise a jour de la population
        population = elitistUpdate(population, childs,data)
        
        #print(population)
        #print(findBestSolution(population))

    # temps fin exec algo
    t2=time.time()
        
    # Resultats

    bestSol, bestObj = findBestSolution(population,data)
        
    print("Population:")
    print(population)
    print() 

    print("CPU Time (s)")
    timePassed = (t2-t1)
    print("%.2f" %timePassed)

    return population[bestSol],bestObj


sol,makespan=AG("./core/data/data.txt")
print("----------------------------------------")
print("ordonnancement",sol)
print("----------------------------------------")
print("fin d'execution t=",makespan)
print("----------------------------------------")