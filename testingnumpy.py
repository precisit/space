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

re = 6371e3
r = (re + 300000)*np.array([1.,0,0])
m = 9000
steps = 1000.
ttot = 15000.
t = 0
dt = ttot/steps
i = 0
v = np.array([0.,7788.,0.])
rsave = np.empty([steps,3])
vsave = np.empty([steps,3])

while (i < steps) :
	if (t>3500 and t<3600):										#initiate burn at 70% of elapsed test time
		a = gravForce(m,r)/m +20*np.array([0.,0.,1.])#10*v/(math.sqrt(np.dot(v,v)))
	else:
		a = gravForce(m,r)/m
	

	v = v + a*dt

	r = r + v*dt

	rsave[i,:] = r 
	vsave[i,:] = v 
	t = t + dt
	i = i + 1


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_zlim(bottom=-(re + 320000), top=(re + 320000))
ax.set_ylim(bottom=-(re + 320000), top=(re + 320000))
ax.set_xlim(left=-(re + 320000), right=(re + 320000))

theta = np.linspace(0.,2*math.pi,100)
phi = np.linspace(0.,math.pi,100)
x = re * np.outer(np.cos(theta), np.sin(phi))
y = re * np.outer(np.sin(theta), np.sin(phi))
z = re * np.outer(np.ones(np.size(theta)), np.cos(phi))

ax.scatter(rsave[:,0],rsave[:,1],rsave[:,2],s=2,c='r')
ax.plot_surface(x,y,z)
plt.show()