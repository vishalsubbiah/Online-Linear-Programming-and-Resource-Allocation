import numpy as np
from cvxpy import *
from random import random, randrange,uniform,normalvariate
from math import sqrt
from ggplot import *
import pandas as pd
##################################################################
k=8
m=1
n=3
x = Variable(k,1)
s = Variable(m,1)
z = Variable(1)

a = np.random.randint(1, 2, (k, m)) #np.random.randint(0,2,(k,m))
p = np.random.uniform(0, 1, (m,1))
q = np.random.randint(10, 21, (k,1))
pi = a.dot(p) + np.sqrt(0.2) * np.random.randn(k, 1)
w=10
obj1 = Maximize(pi.transpose()*x -z + w*sum(log(s))/m)
obj2 = Maximize(pi.transpose()*x -z + w*sum(1-exp(-s))/m)


##################################################################
###offline####
constraints = [a.transpose()*x  - z + s == 0.0, x <= q, x >= 0.0, s >= 0.0]
# Form objective.
# Form and solve problem.
prob1 = Problem(obj1, constraints)
prob1.solve(solver=CVXOPT)  # Returns the optimal value.
print "status:", prob1.status
print "optimal value", round(prob1.value,2)
x_opt = [ round(elem, 2) for elem in x.value ]
print "optimal var", x_opt
offline_x = x_opt
offline_v = round(prob1.value, 2)
##################################################################
###online####
#part 1
constraints = [x[n:] == 0.0,a.transpose()*x  - z + s == 0.0, x <= q, x >= 0.0, s >= 0.0]
# Form objective.
# Form and solve problem.
prob1 = Problem(obj1, constraints)
prob1.solve(solver=CVXOPT)  # Returns the optimal value.
print "status:", prob1.status
print "optimal value", round(prob1.value,2)
x_opt = [ round(elem, 2) for elem in x.value ]
print "optimal var", x_opt

#part 2 version A
c = x[0:n]
constraints = [x[0:n] - c == 0,a.transpose()*x  - z + s == 0, x <= q, x >= 0, s >= 0]
# Form and solve problem.
prob2 = Problem(obj1, constraints)
prob2.solve(solver=CVXOPT,abstol=1e-25)  # Returns the optimal value

#part 2 version B
online_v = []
for l in range(n,k-1):
    c = x[0:l]
    constraints = [x[0:l] - c == 0.0,x[l+1,:]== 0, a.transpose()*x  - z + s == 0.0, x <= q, x >= 0.0, s >= 0.0]
# Form and solve problem.
    prob2 = Problem(obj1, constraints)
    prob2.solve(solver=CVXOPT,abstol=1e-25)  # Returns the optimal value.
    online_v.append(round(prob2.value, 2))

###############
#final output

print "status:", prob2.status
print "optimal value", round(prob2.value,2)
x_opt = [ round(elem, 2) for elem in x.value ]
print "optimal var", x_opt
online_x = x_opt

#######################################Plotting####################################################

iterations = range(n, k-1, 1)
data = pd.DataFrame({'iterations': iterations, 'offline': offline_v, 'online': online_v})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(y = "Opt_values", title = "Optimal Objs")

vals = [np.absolute(online_v[i] - offline_v) for i in range(len(online_v))]
data = pd.DataFrame({'iterations': iterations, 'diff': vals})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(y = "Difference in optimal Objs")

iterations = range(k)
data = pd.DataFrame({'iterations': iterations, 'offline': offline_x, 'online': online_x})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) + labs(y = "Opt_x_values")

vals = [np.absolute(online_x[i] - offline_x[i]) for i in xrange(len(offline_x))]
data = pd.DataFrame({'iterations': iterations, 'diff': vals})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(y = "Difference in optimal x values")

#print (qplot(iterations, offline_v, geom = "line"))
#print (qplot(iterations, online_v, geom = "line"))

