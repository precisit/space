import requests
import json
import numpy as np
import time as timer
import matplotlib.pyplot as plt

We = np.array([0,0,np.pi*2./(24*3600)])
Re = 6371000.

def surfToInertPos(ri,t):
	omega = np.linalg.norm(We)
	Rot = np.array([[np.cos(-omega*t), -np.sin(-omega*t), 0], 
					[np.sin(-omega*t), np.cos(-omega*t), 0],
					[0, 0, 1]])
	rr = np.dot(ri,Rot)
	return rr



url = "http://labs.simulations.io/rocketSim"

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
utdata = requests.post(url,json.dumps(param))
print "time to compute", timer.time() - startComp 
data = utdata.json()

altitudes = np.linalg.norm(data['position'],axis=0) - Re
speed = np.linalg.norm(data['velocity'],axis=0)
t = time = np.array(data['time'])
mass = np.array(data['mass'])
thrust = np.array(data['thrust'])
drag = np.array(data['drag'])
downrange = data['downrange']

numsteps = len(time)
launchpos = np.zeros((3, numsteps))
initpos = np.array( [data['position'][0][0], data['position'][1][0],data['position'][2][0]])

print initpos
for i in range(numsteps):
	launchpos[:,i] = surfToInertPos(initpos,time[i])


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
circ = plt.Circle((0,0), radius=Re, color='b')
ax.add_patch(circ)
plt.plot(data['position'][0], data['position'][1])
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

plt.subplot(3,1,1)
plt.plot(t, thrust)
plt.ylabel("thrust [N]")

plt.subplot(3,1,2)
plt.plot(t, drag)
plt.ylabel("drag [N]")

plt.subplot(3,1,3)
plt.plot(t, (thrust-drag)/(mass*9.81))
plt.ylabel("G-force by thrust and drag")
plt.show()

print data['draglosses'], data['deltaV']