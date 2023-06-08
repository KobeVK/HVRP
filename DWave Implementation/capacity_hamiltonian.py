import os
import itertools
import click
import pandas as pd
from dwave.system import LeapHybridCQMSampler
from dimod import ConstrainedQuadraticModel, BinaryQuadraticModel, QuadraticModel


def parse_inputs(filename, capacity):
    df = pd.read_csv(filename, names=['weight', 'value'], header=None)

    if not capacity:
        capacity = int(0.8 * sum(df['weight']))

    print('weights:', df['weight'])
    print('values:', df['value'])
    print('capacity:', capacity)

    return df['weight'], df['value'], capacity

def build_capacity_cqm(weight, value, capacity):
    num_items = len(weight)
    print('num items:', num_items)
    cqm = ConstrainedQuadraticModel()
    obj = BinaryQuadraticModel(vartype='BINARY')

    # 0 < max(|HB|) < A             -- hyper-parameters
    tot_weight = sum(value)
    B, A = 5, 6*tot_weight

    
    # HA: capacity constraint
    # linear term
    for i in range(capacity):
        obj.add_variable('BINARY', i)
        obj.set_linear(i, -2*A)

    # quad term
    for i in range(capacity):
        for j in range(capacity):
            if i == j: continue     # why??
            obj.set_quadratic(i, j, A * (1 + (i+1)*(j+1)))
    
    for i in range(num_items):
        obj.add_variable('BINARY', i + capacity)
        for j in range(capacity):
            obj.set_quadratic(i + capacity, j, -2*A*weight[i])
    
    for i in range(num_items):
        for j in range(num_items):
            if i == j: continue     # why??
            obj.set_quadratic(i[ + capacity, j + capacity, A * weight[i] * weight[j])
        ]
    # HB: value maximization
    for i in range(num_items):
        obj.set_linear(i+capacity, -B*value[i])

    cqm.set_objective(obj)

    return cqm



def parse_solution(sampleset, weights, values, capacity):
    feasible_solutions = sampleset.filter(lambda row: row.is_feasible)

    if not len(feasible_solutions):
        raise ValueError('No feasible solution found')
    
    best = feasible_solutions.first
    print('best solution:')
    print(best)

    # selected_items = [key for key, value in best.sample.items() if value==1.0 and key >= capacity]
    selected_item_indices = [key for key, val in best.sample.items() if val==1.0]
    print('selected items:', selected_item_indices)
    selected_weights = list(weights.loc[selected_item_indices])
    selected_values  = list(values.loc[selected_item_indices])

    knapsack_weight = [key for key, value in best.sample.items() if value==1.0 and key < capacity]

    print('found best solution at energy', best.energy)
    print('simulated knapsack weight:', knapsack_weight)
    
    print('selected items:', selected_item_indices)
    print('weight of selected items', selected_weights)
    print('total weight', sum(selected_weights))
    print('values of selected items', selected_values)
    print('total value', sum(selected_values))


#############################################################################################

def main(filename, capacity):
    sampler = LeapHybridCQMSampler()

    filename = 'capacity - hvrp/data/very_small.csv'
    capacity = None
    weights, values, capacity = parse_inputs(filename, capacity)

    cqm = build_capacity_cqm(weights, values, capacity)

    print(f'Submitting CQM to solver {str(sampler.solver.name)}')
    sampleset = sampler.sample_cqm(cqm, label='Capacity Hamiltonian')

    print('parsing solution')
    parse_solution(sampleset, weights, values, capacity)




if __name__ == '__main__':
    filename = 'capacity - hvrp/data/very_small.csv'
    capacity = 9
    main(filename, capacity)