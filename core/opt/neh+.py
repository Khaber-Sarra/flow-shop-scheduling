import pandas
import numpy as np

from cmax import cmax
from loader import loader


def neh(data, nb_jobs):
    # TODO add dynamic  nb_machines
    cmax_t = 9999999
    '''
    the parameter of the function needs to be a dataframe in order to 
    minimize the calculation by using Pandas built-in functions 
    :) 
    '''
    mem_jobs_list = []
    partiel_jobs_list, res, tmp_list = [], [], []
    data['jid'] = data.index.copy()

    data['sum'] = data.drop('jid', axis=1).sum(axis=1)
    # data.sort_values(['sum'],ascending=False,inplace = True)
    data.sort_values(['sum'], ascending=False, inplace=True)
    data.reset_index(drop=False)
    jobs = data.to_numpy()

    mem_jobs_list.append(jobs[0])

    for j in jobs[1:]:
        cmax_t = 9999999
        for i in range(len(mem_jobs_list) + 1):
            partiel_jobs_list = mem_jobs_list
            tmp_list = np.insert(partiel_jobs_list, i, j, axis=0)
            c = cmax(tmp_list, nb_jobs)
            if c < cmax_t:
                res = tmp_list
                cmax_t = c
        mem_jobs_list = res
    #print(mem_jobs_list, cmax_t)
    """
    étape 6 de  NEH Amélioré, voir " Amélioration de la NEH " pour plus de détails.
    """

    tmp_list = []
    for i in range(nb_jobs):
        for j in range(i+1,nb_jobs):
            tmp_list = mem_jobs_list.copy()
            tmp_list[i], tmp_list[j] = mem_jobs_list[j], mem_jobs_list[i]
            c = cmax(tmp_list, nb_jobs)
            if c < cmax_t:
                res = tmp_list
                cmax_t = c

    mem_jobs_list = res


    return mem_jobs_list, cmax_t


"""
for testing just uncomment the two lines below 
and modify the data.txt file and the number of jobs
"""

data = loader("../data/data.txt")
neh(data, 4)
