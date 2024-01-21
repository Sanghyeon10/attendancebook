import pandas as pd

ROE = 5
PBR = 3.4
N=5

r= (1+ROE)/ (PBR**(1/N)) - 1

print(r)