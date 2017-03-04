import numpy as np
from cvxpy import *

# Create two scalar optimization variables.
m = 10
K = 10000

A = np.random.randint(0, 2, (m, K))

X = Variable(K)
z = Variable()

q = np.random.randint(10, 21, (K,1))
p = np.random.uniform(0, 1, (m,1))
pi = p.T.dot(A) + np.sqrt(0.2) * np.random.randn(1, K)

A = np.random.randint(0, 2, (m, K))

#randomVector = numpy.random.rand(1, 5);
#scaledRandomVector = numpy.multiply(randomVector, 0.2);
#pi = numpy.add(numpy.array([0.75, 0.35, 0.4, 0.95, 0.75]), scaledRandomVector);

constraints = [];

print A.shape

for i in range(A.shape[0]):
    constraints.append( A[i,:]*X - z <= 0 );

    
for j in range(A.shape[1]):
    constraints.append(X[j] >= 0);
    constraints.append(X[j] <= q[j]);

# Form objective.
obj = Maximize( pi*X - z );

# Form and solve problem.
prob = Problem(obj, constraints)
prob.solve()  # Returns the optimal value.
print "status:", prob.status
print "optimal value", prob.value
print "optimal var:"
print X.value
