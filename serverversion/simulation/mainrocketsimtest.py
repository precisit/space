import mainrocketsim as mr
#import matplotlib.pyplot as plt
import atmofunc
import numpy as np
import time as timer

Re = 6371000.
param = {'rocket':'falcon9', 'payload':17000, 'lat':0, 'tAlt':150000, 'gmax':5,
								'optional':{'draglosses':True, 'thrust':True, 'gravlosses':True, 'downrange':True, 'drag':True}, 
								'pitchAlt':10000, 'pitchT':1, 'initAng':5, 'pitchAng':45,
								'tmax':8000,'dt':1}
param1 = {'rocket':'custom', 'payload':10000, 'lat':0, 'tAlt':150000000, 'gmax':999,
								'optional':{'draglosses':True, 'thrust':True, 'gravlosses':True, 'downrange':True}, 
								'pitchAlt':12000, 'pitchT':1, 'initAng':0, 'pitchAng':45,
								'tmax':20000,'dt':0.5}

param1['stats'] = {'mw1':100000, 'md1':1, 'mi1':1, 'isp1v':500, 'isp1sl':490, 'thr1sl':9999e3, 
					'mw2':10000, 'md2':1, 'mi2':1, 'isp2v':700, 'thr2v':999e3,'Aflow':10}
param2 = {'rocket':'saturnV', 'payload':40000, 'lat':0, 'longi':45, 'tAlt':400000}
startComp = timer.time()
data=mr.RocketSimulator(param)
print "time to compute", timer.time() - startComp 


altitudes = np.linalg.norm(data[0],axis=0) - Re
speed = np.linalg.norm(data[1],axis=0)
t = time = np.array(data[2])
mass = np.array(data[3])
thrust = np.array(data[7])
drag = np.array(data[8])
print drag
downrange = data[9]

numsteps = len(data[2])
launchpos = np.zeros((3, numsteps))
initpos = np.array( [data[0][0][0], data[0][1][0],data[0][2][0]])

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
plt.plot(time,downrange)
plt.show()

plt.subplot(3,1,1)
plt.plot(t,altitudes)
plt.ylabel("altitude [m]")
#plt.subplot(4,1,2)
#plt.plot(t,beta*180/np.pi)
#plt.ylabel("angle to horizon, beta [deg]")

plt.subplot(3,1,2)
plt.plot(t,speed)
plt.ylabel("speed [m/s]")

plt.subplot(3,1,3)
#drymasstot = np.ones((numsteps,1))*(R.md3+R.mi3+R.mp)
plt.plot(t,mass)#,t,drymasstot)
plt.ylabel("mass [kg]")
plt.xlabel("time [s]")

plt.show()
"""
plt.subplot(3,1,1)
plt.plot(t,apsis[0]-Re)
plt.ylabel("periapsis-Re [m]")
plt.subplot(3,1,2)
plt.plot(t,apsis[1]-Re)
plt.ylabel("apoapsis-Re [m]")
plt.subplot(3,1,3)
plt.plot(t,apsis[2]-Re)
plt.ylabel("orthdist-Re [m]")
plt.show()
"""
plt.subplot(3,1,1)
plt.plot(t, thrust)
plt.ylabel("thrust [N]")
"""
plt.subplot(2,1,2)
plt.plot(t,deltaV)
plt.ylabel("applied deltaV [m/s]")
plt.xlabel("time [s]")
"""
plt.subplot(3,1,2)
plt.plot(t, drag)
plt.ylabel("drag [N]")

plt.subplot(3,1,3)
plt.plot(t, (thrust-drag)/(mass*9.81))
plt.ylabel("G-force by thrust and drag")
plt.show()
"""
plt.plot(t, draglosses)
plt.ylabel("Draglosses ")
plt.xlabel("time [s]")
plt.show()
"""
"""
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
circ = plt.Circle((0,0), radius=Re, color='b')
ax.add_patch(circ)
plt.quiver(transPos[0], transPos[1],tang[0],tang[1])
plt.show()

plt.plot(t, gravlosses)
plt.show()
"""
print data[4], data[5]