"""
l'implementation du recherche tabu

"""
import sys
from neh import neh
from neh_improved import neh_i
from loader import  loader
from itertools import  combinations
from cmax import  import cmax

"""
def ts(data, nb_jobs, max_iteration, use_improved_neh=False):
    iter = max_iteration
    H = 10
    obj_best = 9999
    type = 1
    seed = 2458

    # la solution initiale
    #x_init, obj_init = neh(data,nb_jobs)
    x = x_init
    obj = obj_init
    obj_local = 99999


    for i in range(max_iteration):

        obj_y
        if obj_y < obj_local :
            x_local = y
            obj_local = obj_y
            x = y
"""

def swapMove(data,i,j):
    # prend une liste jobs (solution) et retourne un voisin de la solution
    data_c = data.copy() # utilisation d"une copie
    data_c[i], data_c[j] = data[j], data[i]     # swapping
    return  data_c
"""   """

def TSearch(data,tenur, nb_jobs):
    MAX_INT = sys.maxsize
    # les solutions initiales trouvees par NEH
    best_sol, best_objval = neh(data,nb_jobs)
    current_sol, current_objval = best_sol, best_objval

    nb_machines = len(best_sol[0])-1

    # la creation de l'index des jobs pour accelerer l'acces
    job_index = {}
    for i in range(nb_jobs):
        print(best_sol[i])
        job_index[best_sol[i][nb_machines]] = i

    # initialisation de la structure taboue
    tabu_struct = {}
    for swap in combinations(range(nb_jobs), 2):
        tabu_struct[swap] = {"times" : 0, "valeur" : 0}


    iter = 1

    Terminate = 0

    while Terminate < 100 :
        #la fouille de tout le voisinage de la solution courante
        candidat_objval = MAX_INT
        for move in tabu_struct :
            candidat_sol = swapMove(current_sol, move[0], move[1])
            candidat_objval = cmax(candidat_sol,nb_machines)
            tabu_struct[move]['value'] = candidat_objval


        # un mouvement admissible
        while True :
            #selectionner le voisin avec la plus petite valeur
            best_move = min(tabu_struct,key=lambda x : tabu_struct[x]['valeur'])
            best_move_value = tabu_struct[best_move]['valeur']
            tabu_time = tabu_struct[best_move]['times']

            # si non taboue
            if tabu_time < iter :
                #executer le swap
                current_sol = swapMove(current_sol, move[0], move[1])
                current_objval = tabu_struct[best_move]['valeur']

                # si la nouvelle solution est meilleur que la solution existante
                if best_move_value < best_objval :
                    best_sol = current_sol
                    best_objval = current_objval

                    Terminate = 0

                else:

                    Terminate+1

                #mise a jour du tabou
                tabu_struct[best_move]['times'] = iter + tenur
                iter +=1
                break
            #si taboue
            else :
                #aspiration ?
                if best_move_value < best_objval :
                    # appliquer le move :
                    current_sol = swapMove(current_sol, move[0], move[1])
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









data = loader("../data/data.txt")
TSearch(data,3,4)