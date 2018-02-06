import numpy as np

a = np.array([1,2,3,4,5,6,7,8,9,10])
b = a
z = np.polyfit(a,b,1)
print(z)
