import pandas
import numpy as np
from loader import loader
from cmax import cmax


def neh(data):
    # TODO add dynamic  nb_machines
    nb_jobs = 5
    cmax_t = 9999999
    '''
    the parameter of the function needs to be a dataframe in order to 
    minimize the calculation by using Pandas built-in functions 
    :) 
    '''
    mem_jobs_list = []
    partiel_jobs_list, res = [], []
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
            tmp = np.insert(partiel_jobs_list, i, j, axis=0)
            c = cmax(tmp, nb_jobs)
            if c < cmax_t:
                res = tmp
                cmax_t = c
        mem_jobs_list = res
    print(mem_jobs_list, cmax_t)
    return mem_jobs_list, cmax_t



"""
for testing just uncomment the two lines below 
and modify the data.txt file
"""

data = loader("../data/data.txt")
neh(data)
