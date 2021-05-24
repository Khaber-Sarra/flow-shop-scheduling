"""
l'implementation du recherche tabu

"""

from neh import neh
from neh_improved import neh_i
from loader import  loader
from itertools import  combinations

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

def TSearch(data_,tenur,nb_jobs):

    data_['jid'] = data_.index.copy()
    data = data_.to_numpy()

    nb_machines = len(data[0])

    # la creation de l'index des jobs pour accelerer l'acces


    # initialisation de la structure taboue
    tabu_struct = {}
    for swap in combinations(range(nb_jobs), 2):
        tabu_struct[swap] = {"times" : 0, "value" : 0}





    # les solutions initiales trouvees par NEH
    best_sol, best_objval = neh(data,4)
    current_sol, current_objval = best_sol, best_objval

    job_index = {}
    for i in range(nb_jobs):
        job_index[data[i][nb_machines-1]] = i;
    print(job_index)
    print(tabu_struct)

    # iter = 1
    #
    # Terminate = 0
    #
    # while Terminate < 100 :
    #
    # #la fouille de tout le voisinage de la solution courante
    #     for i in range(nb_jobs) :
    #         for j in range(i,nb_jobs):
    #
    #








data = loader("../data/data.txt")
TSearch(data,3,4)