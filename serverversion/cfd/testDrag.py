import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('C:/Github/space/simulation2/RESTAPIs')
import atmofunc
n = 500
v = np.zeros((3,n))
v[0,:] =  np.ones((1,n))*-465.1
v[1,:] = np.linspace(0,150,n)
pos = np.zeros((3,n))
pos[1,:] =  np.ones((1,n))*6371000
vAbs = np.linspace(0,150,n)
alt = 0
CD = np.zeros((n,1))
dragForce = np.zeros((n,1))
for i in range(n):
	CD[i] = atmofunc.dragCoefficient(vAbs[i],alt)
	dragForce[i] = atmofunc.dragForce(v[:,i],pos[:,i],A=21.24)


vabsmeas = np.array([10,50,75,100,150])
CDmeas = np.array([0.34,0.34,0.33,0.33,0.33])
dragForcemeas = np.array([424., 10628, 23860, 41631,95507])
p1 = plt.plot(vAbs,CD)
plt.title('dragCoefficient')
p2 = plt.plot(vabsmeas,CDmeas,'r+')
plt.legend(["braeunigs saturn V","simulated CFD"],loc=7)
plt.xlabel('speed [m/s]')
plt.show()
p3 = plt.plot(vabsmeas,dragForcemeas,'r+')
p4 = plt.plot(vAbs,dragForce)
plt.legend(["simulated CFD", "braeunigs saturn V"],loc=2)
plt.title('dragForce')
plt.ylabel('dragForce [N]')
plt.xlabel('speed [m/s]')
plt.show()

