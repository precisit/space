import matplotlib.pyplot as plt
import numpy as np
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


vabsmeas = np.array([10,95,100])
CDmeas = np.array([0.29,0.53,0.36])
dragForcemeas = np.array([365., np.NaN, 45450])
plt.plot(vAbs,CD)
plt.plot(vabsmeas,CDmeas,'r+')
plt.show()
plt.plot(vabsmeas,dragForcemeas,'r+')
plt.plot(vAbs,dragForce)
plt.show()

