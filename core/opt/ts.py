"""
l'implementation du recherche tabu

"""
import time
import sys
from neh import neh
from neh_improved import neh_i
from loader import loader
from itertools import combinations
from cmax import cmax


def swapMove(data, i, j, jobs_index):
    # prend une liste jobs (solution) et retourne un voisin de la solution
    data_c = data.copy() # utilisation d"une copie
    data_c[[jobs_index[i], jobs_index[j]]] = data_c[[jobs_index[j], jobs_index[i]]]     # swapping
    # MAJ des positions des jobs
    jobs_index[i], jobs_index[j] = jobs_index[j], jobs_index[i]
    return data_c



def tabu_search(data, tenur, nb_jobs):
    MAX_INT = sys.maxsize
    # les solutions initiales trouvees par NEH
    best_sol, best_objval = neh(data,nb_jobs)
    current_sol, current_objval = best_sol, best_objval

    nb_machines = len(best_sol[0])-1

    # la creation de l'index des jobs pour accelerer l'acces
    jobs_index = {}
    for i in range(nb_jobs):
        #print(best_sol[i])
        jobs_index[best_sol[i][nb_machines]] = i

    # initialisation de la structure taboue
    tabu_struct = {}
    for swap in combinations(range(nb_jobs), 2):
        tabu_struct[swap] = {"times" : 0, "valeur" : 0}


    iter = 1

    Terminate = 0

    while Terminate < 10 :
        #la fouille de tout le voisinage de la solution courante
        candidat_objval = MAX_INT
        for move in tabu_struct :
            candidat_sol = swapMove(current_sol, move[0], move[1], jobs_index)
            candidat_objval = cmax(candidat_sol,nb_machines)
            tabu_struct[move]['valeur'] = candidat_objval


        # un mouvement admissible
        while True :
            print("move")
            #selectionner le voisin avec la plus petite valeur
            best_move = min(tabu_struct,key=lambda x : tabu_struct[x]['valeur'])
            best_move_value = tabu_struct[best_move]['valeur']
            tabu_time = tabu_struct[best_move]['times']

            # si non taboue
            if tabu_time < iter:
                #executer le swap
                current_sol = swapMove(current_sol, best_move[0], best_move[1], jobs_index)
                current_objval = tabu_struct[best_move]['valeur']

                # si la nouvelle solution est meilleur que la solution existante
                if best_move_value < best_objval :
                    best_sol = current_sol
                    best_objval = current_objval

                    Terminate = 0

                else:

                    Terminate +=1

                #mise a jour du tabou
                tabu_struct[best_move]['times'] = iter + tenur
                iter +=1
                break
            #si taboue
            else :
                #aspiration ?
                if best_move_value < best_objval :
                    # appliquer le move :
                    current_sol = swapMove(current_sol, best_move[0], best_move[1], jobs_index)
                    current_objval = tabu_struct[best_move]['valeur']
                    best_sol = current_sol
                    best_objval = current_objval

                    Terminate = 0
                    iter += 1

                    break

                else:
                    #taboue sans satisfaire la condition de aspiration
                    tabu_struct[best_move]['valeur'] = MAX_INT  # inadmissible

                    continue

    return  best_sol, best_objval



# TODO : update the swapping function's code to support the jobs' index structure
# TODO : add the choice to use neh_i instead of the classic neh







start=time.time()
data = loader("../data/tai20_20.txt")
sol, makespan=tabu_search(data,3,20)
end=time.time()
print("ordonnancement",sol)
print("----------------------------------------")
print("fin d'execution t=",makespan)
print("----------------------------------------")
print("le temps d'exec algorithme",end-start)