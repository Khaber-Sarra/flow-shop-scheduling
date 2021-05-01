import numpy
from loader import loader

def Chen(dataset):

    Som=[]
    Inf=[]
    Sup=[]
    #lire les donnees depuis le nom de fichier en entrée "Dataset"
    data = loader(dataset,machines_in_rows=False)
    print(data)
    #calculer la somme des temps d'execution de chaque job sur toutes les machines dans Som
    Som=data.sum(axis=1).tolist()
    print(Som)
    #recuperer le job avec le temps d'exec max  
    maxIndex=Som.index(max(Som)) # C
    print("maxIndex",maxIndex)
    n,m=data.shape
    #creer deux liste : Inf contenant les jobs avec P1<=Pm  et Sup contenant les jobs avec P1>Pm
    for i in range(n):
        if (i != maxIndex):
            if (data.iloc[i,0]<=data.iloc[i,m-1]):
                Inf.append([data.iloc[i,0],i])
            else :
                Sup.append([data.iloc[i,m-1],i])
    #trier la liste Inf selon l'ordre croissant de P1
    Inf=sorted(Inf,key=lambda x:x[0])
    #trier la liste Sup selon l'ordre décroissant de Pm
    Sup=sorted(Sup,key=lambda x:x[0], reverse=True)
    print("La premiere sequence",Inf)
    print("La deuxieme sequence",Sup)
    sol =[]
    #concatener les liste : Inf, Max, Sup dans la solution finale
    for i in range(len(Inf)):
        sol.append(Inf[i][1])
    sol.append(maxIndex)
    for i in range(len(Sup)):
        sol.append(Sup[i][1])
    #retourner l'ordonnencement final
    return sol

sol=Chen("./core/data/data1.txt")
print("La solution",sol)