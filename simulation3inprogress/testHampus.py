import RocketSim
import RocketClass3stage
import time as timer
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

Re = RocketSim.Re

startTime = timer.time()

R = RocketClass3stage.CreateRocket({'type':'falcon9', 'payload':10000, 'gAlt':10000, 'gmax':100, 'tAlt':200000})
optional = {'draglosses':False,
			'gravlosses':False,
			'thrust':False,
			'drag':False,
			'pitchangle':False}
data = RocketSim.RocketSimulator(R, 90, 45, 1000,1, optional)

"""Plotting 3D"""
	
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(data[0][0],data[0][1],data[0][2], marker='.')
	
	#Plot earth-size sphere
	
phi = np.linspace(0, 2 * np.pi, 100)
theta = np.linspace(0, np.pi, 100)
xm = Re * np.outer(np.cos(phi), np.sin(theta))
ym = Re * np.outer(np.sin(phi), np.sin(theta))
zm = Re * np.outer(np.ones(np.size(phi)), np.cos(theta))
ax.plot_surface(xm, ym, zm)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.show()

print 'Delta-V: ', data[3]
print 'Draglosses: ', data
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
circ = plt.Circle((0,0), radius=Re, color='b')
ax.add_patch(circ)
plt.plot(data[0][0], data[0][1])
plt.show()
print timer.time()-startTime
