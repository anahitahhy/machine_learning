import numpy as np
A = np.array([
    [1,7,3],
    [5,6,9]
])
B = np.array([
    [2,3,5],
    [3,5,6],
    [9,1,6],
    [1,2,9]
])

rows, cols = 3, 2

new_A = np.zeros((rows, cols), dtype=int)


index = 0
for i in range(rows):
    for j in range(cols):
        new_A[i][j] = A[index // 3][index % 3]
        index += 1

result = np.dot(B,new_A)
print(result)