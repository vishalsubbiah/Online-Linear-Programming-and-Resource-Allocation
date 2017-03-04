import numpy as np
from cvxpy import *

m = 10
K = 10000
w = 1e-3

A = np.random.randint(0, 2, (m, K))

s = Variable(m)
x = Variable(K)
z = Variable()

q = np.random.randint(10, 21, (K,1))
p = np.random.uniform(0, 1, (m,1))
Pi = p.T.dot(A) + np.sqrt(0.2) * np.random.randn(1, K)

constraints = [A * x - z + s == 0, x <= q, x >= 0, s >= 0]

u = (w/m) * sum_entries(log(s))
#u = (w/m) * sum_entries(1 - exp(-s)/m)

obj = Maximize(Pi * x - z + u)

prob = Problem(obj, constraints)
prob.solve(solver = CVXOPT)

print "status", prob.status
print "optimal value", prob.value
print "optimal var", x.value





