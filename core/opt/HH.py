import numpy as np
from loader import loader
from Makespan import Makespan
import random
from neh import neh
from Chen import Chen
from STP import STP
from PH import ph


datal=[]
res=0
data=loader("./core/data/tai50_5.txt",machines_in_rows=True)
n,m=data.shape



ord=[]

#generer une combinaison aleatoire d'heuristiques
def Generer_comb_initiale():
    return np.random.permutation(['n','c','p','s']).tolist()


#generer une nouvelle combinaison d'heuristique par swap ou changement de la combinaison courante "com"
def Generer_nouvelle_comb(com,tabu):  
    comb=com.copy()
    while(True):
        choice=random.choice(["swap","change"])
        if (choice=="swap"):
            #on choisit aleatoirement deux positions et on swap les elements correspondants
            pos = list(np.random.permutation(np.arange(4))[:2])
            remheur = comb[pos[1]]
            comb[pos[1]]=comb[pos[0]]
            comb[pos[0]] = remheur

        else:
            #on choisit une position aleatoirement et on change l'element correspondant par une heuristique aleatoire 
            #dans ce cas on peut avoir des doublons dans notre combinaison
            index=random.choice([0,1,2,3])
            newheu=random.choice(['n','c','p','s'])
            comb[index]=newheu
        
        
        if (comb not in tabu):
            #seulement si la combinaison générée n'est pas dans la liste tabu, on sort de la fct
            break
        
    return comb
  

#recuperer l'ordonnancement des jobs a partir d'une combinaison d'heuristique "comb"
#'datal' contient la matrice des jobs/machines divisée sur 4 (le nbr d'heuristiques) 
def get_ord(comb,datal):
    sol=[]
    n,m=data.shape
    for i in range(len(comb)):
        heur=comb[i]
        '''
        on parcours les heuristiques selon leurs aparitions dans 'comb'
        et on recupere l'ordonnancement trouvé par l'heuristique pour la partie de la matrice job/machines
        qui se trouve a la ieme position dans 'datal'  
        '''
        if (heur=='n'):
            ord,list,cmax=neh(datal[i],n,m)
            ord= ord.tolist()
            sol=sol+ord
            
        elif (heur=='c'):
            ord,mak=Chen(datal[i])
            #ici on rajoute le nbr de jobs deja ordonnés par les heuristiques qui precedent l'heuristique courante dans comb
            #car par ex si on a 20 jobs en premier lieu, et on a la combinaison ['p','n','c','s']
            #l'heuristique chen va ordonner 5 jobs mais les jobs dans la sequence retournée sont compris entre 0 et 4
            #donc on rajoute les 10 jobs deja traité par palmer et Neh 
            ord= [x+len(sol) for x in ord]
            sol=sol+ord
            
        elif (heur=='p'):
            ord,span=ph(datal[i])  
            ord= [x+len(sol) for x in ord]
            sol=sol+ord  

        else:
            ord,ma=STP(datal[i]) 
            ord= [x+len(sol) for x in ord]
            sol=sol+ord
                
    return sol        


def HH(dataset,nb_it_max,nb_it_sansAme):
   
    comb=[]
    tabu=[]
    nb=0 #compteur d'iterations
    nbs=0 #compteur d'iterations sans amelioration
    #diviser la matrice jobs/machines en parties 
    datal=np.array_split(dataset,4)
    comb=Generer_comb_initiale()
    #tabu contient les combinaisons générées
    tabu.append(comb)
    sol1=get_ord(comb,datal)

    while ((nb< nb_it_max)and (nbs<nb_it_sansAme)):
        
        comb=Generer_nouvelle_comb(comb,tabu)
        tabu.append(comb)
        sol2=get_ord(comb,datal)
        if(Makespan(dataset,sol2)<Makespan(dataset,sol1)):
            sol1=sol2
        else:
            nbs=nbs+1
        
        nb=nb+1

    return sol1,Makespan(data,sol1)


nb_it_max=100
nb_it_sansAme=30


sol,make=HH(data,nb_it_max,nb_it_sansAme)
print("la solution est ")
print(sol)

print(make)
