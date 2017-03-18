import numpy as np
from cvxpy import *
from random import random, randrange,uniform,normalvariate
from math import sqrt
from ggplot import *
import pandas as pd
##################################################################
k=10000
m=10
n=1000
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
prob1.solve(solver=SCS)  # Returns the optimal value.
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
prob1.solve(solver=SCS)  # Returns the optimal value.
print "status:", prob1.status
print "optimal value", round(prob1.value,2)
x_opt = [ round(elem, 2) for elem in x.value ]
print "optimal var", x_opt

#part 2 version A
c = x[0:n]
constraints = [x[0:n] - c == 0,a.transpose()*x  - z + s == 0, x <= q, x >= 0, s >= 0]
# Form and solve problem.
prob2 = Problem(obj1, constraints)
prob2.solve(solver=SCS)  # Returns the optimal value
online_v_1 = round(prob1.value, 2)
online_x_1 = [round(elem,2) for elem in x.value]

#part 2 version B
online_v_2 = []
for l in range(n,k-1):
    c = x[0:l]
    constraints = [x[0:l] - c == 0.0,x[l+1,:]== 0, a.transpose()*x  - z + s == 0.0, x <= q, x >= 0.0, s >= 0.0]
# Form and solve problem.
    prob2 = Problem(obj1, constraints)
    prob2.solve(solver=SCS)  # Returns the optimal value.
    online_v_2.append(round(prob2.value, 2))
    print l

###############
#final output

print "status:", prob2.status
print "optimal value", round(prob2.value,2)
x_opt = [ round(elem, 2) for elem in x.value ]
print "optimal var", x_opt
online_x_2 = x_opt

#######################################Plotting####################################################

iterations = range(n, k-1, 1)
data = pd.DataFrame({'iterations': iterations, 'offline': offline_v, 'online_2': online_v_2})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(y = "Optimal Objectives")

data = pd.DataFrame({'iterations': iterations, 'online_1': online_v_1, 'online_2': online_v_2})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(y = "Optimal Objectives")

vals = [np.absolute(online_v_1 - offline_v)] * len(online_v_2)
data = pd.DataFrame({'iterations': iterations, 'diff': vals})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(title = "Absolute Difference in Optimal Objectives for online model 1 with offline model")

vals = [np.absolute(online_v_2[i] - offline_v) for i in range(len(online_v_2))]
data = pd.DataFrame({'iterations': iterations, 'diff': vals})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(title = "Absolute Difference in Optimal Objectives for online model 2 with offline model")

iterations = range(k)
data = pd.DataFrame({'iterations': iterations, 'offline': offline_x, 'online_1': online_x_1, 'online_2': online_x_2})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(y = "Optimal x values")

vals = [np.absolute(online_x_1[i] - offline_x[i]) for i in xrange(len(online_x_1))]
data = pd.DataFrame({'iterations': iterations, 'diff': vals})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(title = "Absolute Difference in Optimal x values for online model 1 with offline model")

vals = [np.absolute(online_x_2[i] - offline_x[i]) for i in xrange(len(online_x_2))]
data = pd.DataFrame({'iterations': iterations, 'diff': vals})
data = pd.melt(data, id_vars = 'iterations')
print (ggplot(data, aes(x = 'iterations', y = 'value', colour = 'variable')) + geom_line()) +\
        labs(title = "Absolute Difference in Optimal x values for online model 2 with offline model")

#print (qplot(iterations, offline_v, geom = "line"))
#print (qplot(iterations, online_v, geom = "line"))


