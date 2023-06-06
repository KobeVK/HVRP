from common import *


#importing knapsack values and weights
file_path = 'small_data'
values, weights = parse_data(file_path)

# Setting up capacity
capacity_truck1 = 100
capacity_truck2 = 20

# Set capacities using the set_truck_capacity function
set_truck_capacity(truck1, capacity_truck1)
set_truck_capacity(truck2, capacity_truck2)

print(truck1['capacity'])

###################################################################################################

