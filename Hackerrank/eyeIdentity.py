import numpy as np


np.set_printoptions(legacy='1.13')
rows, columns = map(int, input().split())
print(np.eye(rows, columns))
