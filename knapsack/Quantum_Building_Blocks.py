from common import *
from qiskit import * 
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.translators import from_docplex_mp
from docplex.mp.model import Model

# import numpy as np
# from qiskit_optimization.algorithms import OptimizationResult
# from qiskit_optimization.problems.quadratic_program import QuadraticProgram
# from .optimization_application import OptimizationApplication


file_path = 'small_data'
values, weights = parse_data(file_path)

#emphasis on which Ha or Hb
#A = 40 (for small data)
#B =  

N = len(weights) + 1  # number of objects
W = 10 # max weight

mdl = Model('docplex model')

z = {}  # Dictionary to store binary variables z
for i in range(1, W+1):
    z[i] = mdl.binary_var('z{}'.format(i))

x = {}  # Dictionary to store binary variables x
for i in range(N):
    x[i] = mdl.binary_var('x{}'.format(i))

L = 0  
for i in range(1, W+1):
    L -= 2 * z[i]

Q = 0
for i in range(1, W+1):
    for j in range(1, W+1):
        Q += z[i] * z[j]

for i in range(1, W+1):
    for j in range(1, W+1):
        Q += i * j * z[i] * z[j]

for i in range(1, W+1):
    for j in range(1, N+1):
        Q += -2 * (i * z[i]) * (weights[j] * x[j])

for i in range(1, N+1):
    for j in range(1, N+1):
        Q += (weights[i]* x[i]) * (weights[j] * x[j])

Hb=0
for i in range(1, N):
    Hb -= (values[i]*x[i])

#Ha+Hb
mdl.minimize(Hb+L+Q)
mod = QuadraticProgram()
op = from_docplex_mp(mdl)
print(mod.export_as_lp_string())


