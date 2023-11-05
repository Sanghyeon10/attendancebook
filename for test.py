from itertools import *

arr= [list(map(int,input()) for _ in range(2))]
print(arr)
N, K= map(int,input().split())
givennubmer=list()

conbination = list(combinations(range(N), K))
givennubmerbest=0

givennubmer= str(givennubmer)
for i in range(len(conbination)):
    for m in range(K):
        givennubmer= givennubmer[:conbination[m]]+" "+givennubmer[conbination[m]+1:]

    givennubmer=int(givennubmer.strip())
    givennubmerbest=max(givennubmer,givennubmerbest)

