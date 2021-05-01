"""

the cmax function that calculates the makespan of a given solution 
the parameter solution is a numpy array object
ex :
[[ 4  8  8  7  2  3 29]
 [ 9  4  5  8  6  2 32]
 [ 5  9  8 10  1  0 33]
 [ 9  3 10  1  8  1 31]]
"""


def cmax(solution, nb_machines):
    nb_jobs = len(solution)

    if nb_jobs == 0 or nb_machines == 0:
        return 0

    else:
        tmp_res = [0]

        for i in range(nb_machines):
            tmp_res.append(tmp_res[i] + solution[0][i])

        for j in range(1, nb_jobs):
            # the 1st machine
            tmp_res[0] = tmp_res[0] + solution[j - 1][0]
            for m in range(1, nb_machines + 1):
                tmp_res[m] = max(tmp_res[m] + solution[j - 1][m], tmp_res[m - 1] + solution[j][m - 1])
    # print(tmp_res[nb_machines])
    return tmp_res[nb_machines]
