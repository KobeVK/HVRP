# To find the solution using classically, goto classical.py
from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

cqm = ConstrainedQuadraticModel()

x = Integer('x', upper_bound=5, lower_bound=-5)
cqm.set_objective((x-1)**2)

sampler = LeapHybridCQMSampler()                
sampleset = sampler.sample_cqm(cqm)  
# print(sampleset.data)


# ------- Print results to user -------
print('-' * 60)

best_result = sampleset.first.sample
print('best result:', best_result)

print('-' * 60)