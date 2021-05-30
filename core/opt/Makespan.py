
def Makespan(data,ord):
    res=[]

    n,m=data.shape
    #le premier job dans ordonnancement ord commence sur la machine1 en t=0
    res.append(0)
    #on calcule les temps de debut sur chaque machine 
    # q le temps debut sur la machine courante = temps debut sur la machine precedente + 
    # temps exec sur machine precedente
    for j in range (m-1):
        res.append(data.iloc[ord[0],j]+res[j])
    #print(res)
    #pour les autres jobs
    for i in range(n-1):
        #le temps debut sur la premiere machine est egal
        res[0]=res[0]+data.iloc[ord[i],0]
        #pour les autres machines
        for j in range(m-1):
            res[j+1]=max(data.iloc[ord[i],j+1]+res[j+1],data.iloc[ord[i+1],j]+res[j])
        print(res)

    #Makespan retourne la fin d'exec du dernier job sur la derniere machine 
    return res[m-1]+data.iloc[ord[n-1],m-1]

