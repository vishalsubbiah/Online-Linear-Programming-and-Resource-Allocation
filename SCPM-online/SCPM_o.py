import numpy as np
from cvxpy import *
from random import random, randrange,uniform,normalvariate
from math import sqrt


k=10000
m=1
n=1000
x = Variable(k,1)
s = Variable(m,1)
z = Variable(1)

a = np.random.randint(0, 2, (k, m))
p = np.random.uniform(0, 1, (m,1))
q = np.random.randint(10, 21, (k,1))
pi = a.dot(p) + np.sqrt(0.2) * np.random.randn(k, 1)
w=1e-3

#part 1
constraints = [x[n:] == 0,a.transpose()*x  - z + s == 0, x <= q, x >= 0, s >= 0]
# Form objective.
obj1 = Maximize(pi.transpose()*x -z + w*sum(log(s))/m)
obj2 = Maximize(pi.transpose()*x -z + w*sum(1-exp(-s))/m)
# Form and solve problem.
prob1 = Problem(obj1, constraints)
prob1.solve(solver=CVXOPT)  # Returns the optimal value.
print "status:", prob1.status
print "optimal value", prob1.value
print "optimal var", x.value


#part 2

b = x[0:n]
constraints = [x[0:n] - b == 0,a.transpose()*x  - z + s == 0, x <= q, x >= 0, s >= 0]
obj1 = Maximize(pi.transpose()*x -z + w*sum(log(s))/m)
obj2 = Maximize(pi.transpose()*x -z + w*sum(1-exp(-s))/m)
# Form and solve problem.
prob2 = Problem(obj1, constraints)
prob2.solve(solver=CVXOPT,abstol=1e-25)  # Returns the optimal value.

print "status:", prob2.status
print "optimal value", prob2.value
print "optimal var", x.value
