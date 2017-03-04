import numpy as np
from cvxpy import *
from random import random, randrange,uniform,normalvariate
from math import sqrt
# Create two scalar optimization variables.

k=10
m=2

x = Variable(k)
s = Variable(m)
z = Variable(1)
pi=np.zeros((k))
a=np.zeros((k,m))
p=np.zeros(m)
q=np.zeros(k)
w=1e-3



for i in range(m):
    p[i]=random()
for i in range(k):
    for j in range(m):
        a[i,j]=randrange(0,2)
    q[i]=randrange(10,21)

for i in range(k):
    pi[i]=sum(a[i,:]*p) + normalvariate(0,sqrt(0.2))


constraints = []
for l in range(k):
    for i in range(m):
        temp_sum=0
        for j in range(k-1):
            temp_sum=temp_sum+a[j,i]*x[j]
        constraints.append(a[l,i]*x[l] - z + s[i] == -temp_sum)
    constraints.append(x[l]<=q[l])
    constraints.append(x[l]>=0)

# Form objective.
obj1 = Maximize(sum(pi*x) -z + w*sum(log(s))/m)
obj2 = Maximize(sum(pi*x) -z + w*sum(1-exp(-s))/m)
# Form and solve problem.
prob = Problem(obj1, constraints)
prob.solve()  # Returns the optimal value.
print "status:", prob.status
print "optimal value", prob.value
print "optimal var", x.value
