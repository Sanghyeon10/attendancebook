import pandas as pd

ROE = 15
PBR = 1.37
N=7

r= (1+ROE)/ (PBR**(1/N)) - 1

print(r)