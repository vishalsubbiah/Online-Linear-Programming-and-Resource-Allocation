import numpy
from cvxpy import *

# Create two scalar optimization variables.
X = Variable(5);
z = Variable();

A = numpy.array([[1,0,1,1,0],[1,0,0,1,1],[1,0,1,1,0],[0,1,0,1,1],[0,0,1,0,0]]);

pi = numpy.array([0.75, 0.35, 0.4, 0.95, 0.75]);
#randomVector = numpy.random.rand(1, 5);
#scaledRandomVector = numpy.multiply(randomVector, 0.2);
#pi = numpy.add(numpy.array([0.75, 0.35, 0.4, 0.95, 0.75]), scaledRandomVector);

q = numpy.array([10, 5, 10, 10, 5]);

# Create two constraints.
constraints = [];

for i in range(A.shape[1]):
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
