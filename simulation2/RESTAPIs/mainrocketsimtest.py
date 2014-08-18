import mainrocketsim as mr
import matplotlib.pyplot as plt
import atmofunc
import numpy as np
Re = 6371000.
param = {'rocket':'falcon9', 'payload':10000, 'lat':0, 'tAlt':200000, 'optional':{'draglosses':True, 'thrust':True, 'gravlosses':True, 'downrange':True}, 'tmax':8000}
param1 = {'rocket':'custom', 'payload':10000, 'lat':0, 'longi':213 ,'tAlt':200000, 'optional':{'draglosses':True, 'thrust':True, 'gravlosses':True}}
param2 = {'rocket':'saturnV', 'payload':40000, 'lat':0, 'longi':45, 'tAlt':400000}
param1['stats'] = {'mw1':100000, 'md1':10000, 'mi1':500, 'isp1v':320, 'isp1sl':300, 'thr1sl':2000000}
data=mr.RocketSimulator(param)

numsteps = len(data[2])
launchpos = np.zeros((3, numsteps))
initpos = np.array( [data[0][0][0], data[0][1][0],data[0][2][0]])
time = np.array(data[2])
print initpos
for i in range(numsteps):
	launchpos[:,i] = atmofunc.surfToInertPos(initpos,time[i])


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
circ = plt.Circle((0,0), radius=Re, color='b')
ax.add_patch(circ)
plt.plot(data[0][0], data[0][1])
plt.plot(launchpos[0],launchpos[1],'r+')
plt.show()
plt.plot(data[2],data[8])
plt.plot(data[2],data[6])
plt.show()



print data[4], data[5]