import datetime
import pandas as pd
import making


# 예시 딕셔너리
d = {"apple": 1, "banana": 2, "cherry": 2, "date": 4}
val = 2

print(next(k for k, v in d.items() if v == 2))   # banana  (방식 1)
print([k for k, v in d.items() if v == 2])       # ['banana', 'cherry']  (방식 2)
inverse = {v: k for k, v in d.items()}
print(inverse[4])                                # date  (방식 3)

