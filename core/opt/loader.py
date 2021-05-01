
import numpy as np
import pandas as pd


'''
a small confusion is that the problem presentation may varies 
sometimes the jobs are presented by lines and other times by the columns 
the default is Machine = 1 Col
if the representation you use is the inverse just pass 
machines_in_rows=True instead of the default value False

'''


def loader(file_name,machines_in_rows=False): 
    # load a given file with the name "file_name"
    data = pd.read_csv(file_name,header=None,delim_whitespace=True)
    data
    if machines_in_rows:
        d=data.transpose()
        return d
    
    
    # the retuen type is a pandas DataFrame 
    return data


# to test the loader just uncomment the next line an give a valid data.txt path
<<<<<<< HEAD:core/loader.py
#print(loader("./data/data.txt"))
=======
# print(loader("../data/data.txt"))
>>>>>>> 84343892dc42826b7ca74d782eb26a383dafe3ab:core/opt/loader.py
