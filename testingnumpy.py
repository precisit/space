import numpy as np
import math
from scipy import constants as consts
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

M = 5.97219e24
def gravForce(m,r):
	normr = math.sqrt(np.dot(r,r))
	F = (-consts.G*M*m/(normr**3))*r
	return F


r = (6371e3 + 200000)*np.array([1.,0,0])
m = 9000
steps = 100.
ttot = 5000.
t = 0
dt = ttot/steps
i = 0
v = np.array([0.,7788.,0.])
rsave = np.empty([steps,3])
vsave = np.empty([steps,3])

while (i < steps) :
	if (i>0.7*steps):										#initiate burn at 70% of elapsed test time
		a = gravForce(m,r)/m +2*v/(math.sqrt(np.dot(v,v)))
	else:
		a = gravForce(m,r)/m
	
	print a
	v = v + a*dt
	print v
	r = r + v*dt
	print r
	print ""
	rsave[i,:] = r 
	vsave[i,:] = v 
	t = t + dt
	i = i + 1


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
"""
ax.set_zlim(bottom=-250000, top=250000)
ax.set_ylim(bottom=-250000, top=250000)
ax.set_xlim(left=-250000, right=250000)
"""
x, y, z = np.meshgrid(np.arange(-300000, 1000, 300000),
                      np.arange(-300000, 1000, 300000),
                      np.arange(-300000, 1000, 300000))

print rsave[:,0]
ax.scatter(rsave[:,0],rsave[:,1],rsave[:,2])
plt.show()