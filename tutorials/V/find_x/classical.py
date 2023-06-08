# imports
import random
import numpy as np 
import matplotlib.pyplot as plt

# Find solution to x+1 = 2

# Classical
# Suppose we know that the x_sol is between -5 and 5
# f: x+1, g: 2  -> find min distance between the two curves
# min ((x+1)-2)^2 = min (x-1)^2

x = [random.uniform(-5, 5) for _ in range(30)]
val = list(map(lambda x: (x-1)**2, x))

x_sol = x[val.index(min(val))]
print('solution is x_sol =', x_sol)

plt.scatter(x, val, marker='x')
plt.savefig('/workspace/DWave/Beginner/find_x/plot')


