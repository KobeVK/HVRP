truck1 = {}
truck2 = {}

def set_truck_capacity(truck, capacity):
    truck['capacity'] = capacity
    
def parse_data(file_path):
    values = []
    weights = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                left, right = line.split()
                values.append(int(left))
                weights.append(int(right))

    return values, weights