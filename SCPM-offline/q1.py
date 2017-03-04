import numpy as np
from cvxpy import *

m = 10
K = 1000
w = 1e-3

A = np.random.randint(0, 2, (m, K))

s = Variable(m)
x = Variable(K)
z = Variable()

q = np.random.uniform(10, 20, (K,1))
p = np.random.uniform(0, 1, (m,1))
Pi = p.T.dot(A) + 0.2 * np.random.randn(1, K)

constraints = [A * x - z + s == 0, x <= q, x >= 0, s >= 0]

u = (w/m) * sum_entries(log(s))

obj = Maximize(Pi * x - z + u)

prob = Problem(obj, constraints)
prob.solve(solver = CVXOPT)

print z.value
print prob.value
print s.value
print x.value





