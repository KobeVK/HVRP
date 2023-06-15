from common import *

def knapsack_solver_classical(file_path, W):
    # Import knapsack values and weights
    values, weights = parse_data(file_path)
    N = len(weights)  # number of objects

    def knapsack_classic(W, wt, v, N):
        K = [[0 for x in range(W + 1)] for x in range(N + 1)]
 
        # Build the K[][] table bottom-up
        for j in range(N + 1):
            for w in range(W + 1):
                if j == 0 or w == 0:
                    K[j][w] = 0
                elif wt[j-1] <= w:
                    K[j][w] = max(v[j-1] + K[j-1][w-wt[j-1]], K[j-1][w])
                else:
                    K[j][w] = K[j-1][w]
        return K[N][W], K

    solution, K = knapsack_classic(W, weights, values, N)
    total_value = solution
    max_weigth = W

    chosen_objects = []
    chosen_values = []
    chosen_weights = []
    j = N
    w = W
    while j > 0 and w > 0:
        if K[j][w] != K[j-1][w]:
            chosen_objects.append(j)
            chosen_values.append(values[j-1])
            chosen_weights.append(weights[j-1])
            w -= weights[j-1]
        j -= 1
    chosen_objects.reverse()
    chosen_values.reverse()
    chosen_weights.reverse()
    chosen_weights_sum = sum(chosen_weights)
    
    #total_objects = len(chosen_objects)
    total_objects = 1

    return chosen_objects, chosen_values, chosen_weights, max_weigth, total_objects, total_value, chosen_weights_sum
