from common import *
from qiskit import *
from qiskit import Aer
import numpy as np
from qiskit_optimization.translators import from_docplex_mp
from docplex.mp.model import Model
import logging
import math
from qiskit.primitives import Sampler
from qiskit.utils import algorithm_globals
from qiskit.algorithms.optimizers import SPSA , COBYLA
from qiskit.algorithms.minimum_eigensolvers import SamplingVQE
from qiskit.circuit.library import RealAmplitudes
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.utils import algorithm_globals, QuantumInstance
from ibm_quantum_widgets import CircuitComposer
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

def knapsack_solver_quantum(file_path, max_weight):
    logger = logging.getLogger(__name__)

    # Importing data
    values, weights = parse_data(file_path)

    N = len(values)  # Number of objects
    if N != len(weights):
        raise ValueError("The values and weights must have the same length")
    if any(v < 0 for v in values) or any(w < 0 for w in weights):
        raise ValueError("The values and weights cannot be negative")
    if all(v == 0 for v in values):
        raise ValueError("The values cannot all be 0")

    if max_weight < 0:
        raise ValueError("max_weight cannot be negative")

    # Create a model
    mdl = Model(name="Knapsack")
    A = 10 * np.sum(values)
    x = {i: mdl.binary_var(name=f"x_{i}") for i in range(N)}

    mdl = Model(name="Knapsack")
    x = {i: mdl.binary_var(name=f"x_{i}") for i in range(N)}
    mdl.maximize(mdl.sum(values[i] * x[i] for i in x))
    mdl.add_constraint(mdl.sum(weights[i] * x[i] for i in x) <= max_weight)
    op = from_docplex_mp(mdl)
    #print(op.export_as_lp_string())

    # Solve and optimize using minimum eigen solver
    algorithm_globals.random_seed = 1234
    seed = 10598
    vqe = SamplingVQE(sampler=Sampler(), optimizer=SPSA(), ansatz=RealAmplitudes())
    optimizer = MinimumEigenOptimizer(min_eigen_solver=vqe)
    optimizer.min_eigen_solver.ansatz
    result = optimizer.solve(op)

    result_str = str(result)
    result_parts = result_str.split(', ')
    x_values = [part for part in result_parts if 'x_' in part]
    
    selected_objects = []
    total_value = 0
    total_weight = 0
    print("Your knapsack will contain:")
    for x in x_values:
        index, is_selected = x.split('=')
        index = int(index.split('_')[1])
        if float(is_selected) == 1.0:
            print(f"Object: {index} - Value: {values[index]} - Weight: {weights[index]}")
            selected_objects.append(index)
            total_value += values[index]
            total_weight += weights[index]

    print(f"The maximum weight the knapsack can have is: {max_weight}")
    print(f"And according to the data provided, we can put {len(selected_objects)} objects inside it")
    print(f"With a total value of {total_value}")
    print(f"And a total weight of {total_weight}")
    
    # backend = Aer.get_backend('aer_simulator_statevector')
    # quantum_instance = QuantumInstance(backend, seed_simulator=seed, seed_transpiler=seed)
    # optimal_qc = vqe.get_optimal_circuit()
    # editor = CircuitComposer(circuit=optimal_qc)
    # editor
    

# data_file = 'data/tiny_data'
# max_knapsack_weight = 25
# knapsack_solver_quantum(data_file, max_knapsack_weight)
