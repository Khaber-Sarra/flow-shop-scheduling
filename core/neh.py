import pandas as pd 


data = pd.read_csv("data.txt",header=None)
data = data.transpose()
print((data))