import numpy as np
from scipy.integrate import odeint
import atmofunc
import math
import matplotlib.pyplot as plt
import scipy.constants as consts
import RocketClass
import OrbitCalculations as OC
import time as timer
import ascTime
# Earth constants
Me = 5.97219e24
Re = 6371000.
We = np.array([0,0,2*math.pi/(24*60*60)])
"""
Functions
"""

def RocketFunc(w, t, rocket):
	pos = np.array([w[0], w[2], w[4]])			# Positions
	vel = np.array([w[1], w[3], w[5]]) 			# Velocities
	velUnit = vel/np.linalg.norm(vel)			# Unit velocity vector
	dragForce = atmofunc.dragForce(vel, pos)	# Drag force magnitude
	rocket.MainController(t)
	thrust = rocket.newThrustGravTurn(pos,vel,t)

	dm = rocket.mcurr-w[6] 						# Mass of the rocket
	dv = np.linalg.norm(thrust)/rocket.mcurr
	dT = np.linalg.norm(thrust)-w[8]
	GravityAcc = GravAcc(pos) 					# Acceleration due to gravity
	acc = (1/rocket.mcurr)*(-dragForce*velUnit + thrust)+GravityAcc

	return [vel[0], acc[0],
			vel[1], acc[1],
			vel[2], acc[2], dm, dv, dT]

def GravAcc(pos):
	""" Calculates the gravitational acceleration at the current position """
	return -pos*consts.G*Me/(np.linalg.norm(pos)**3)

"""
Test program
"""
if __name__ == '__main__':
	startTime = timer.time()
	"""Initial conditions """
	lat = math.radians(0) 									# Latitude
	longi = math.radians(90)								# Longitude
	initPos = Re*np.array([math.cos(lat)*math.cos(longi),
						   math.cos(lat)*math.sin(longi),
						   math.sin(lat)])					# Initial position vector
	initVel = np.cross(We, initPos)							# Initial velocity vector
	payload = 14000.
	initial_conds = [initPos[0], initVel[0], initPos[1], initVel[1], initPos[2], initVel[2],
					 402000+90720+payload, 0, 5885.e3]
	time = np.linspace(0,8000,10000) 	
	"""
	Rocket initial conditions
	"""
	R = RocketClass.Rocket(402000., 16000., 3900., 320., 280., 5885.e3, 90720., 3200., 182., 345., 800000., payload, time[0], 25000., 0.615384615)

	""" End initial conditions """



	solutions = odeint(RocketFunc, initial_conds, time, args=(R,))		# Integrate
	print "time to execute",timer.time()-startTime
	pos = np.array([solutions[:,0], solutions[:,2], solutions[:,4]])
	vel = np.array([solutions[:,1], solutions[:,3], solutions[:,5]])
	mass = solutions[:,6]
	deltaV = solutions[:,7]
	thrust = solutions[:,8]

	altitudes = np.zeros((len(solutions),1))
	speed = np.zeros((len(solutions),1))
	tang = np.zeros((3,len(solutions)))
	beta = np.zeros((len(solutions),1))
	apsis = np.zeros((3,len(solutions)))

	for i in range(len(solutions)):
		altitudes[i] = np.linalg.norm(pos[:,i])-Re
		speed[i] = np.linalg.norm(vel[:,i])
		tang[:,i] = np.cross(pos[:,i],np.cross(vel[:,i],pos[:,i]))
		if (not np.linalg.norm(tang)==0):
			beta[i] = OC.angleVec(vel[:,i],tang[:,i])
		apsis[:,i] = OC.ApsisCalculation(pos[:,i],vel[:,i])
	
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ = plt.Circle((0,0), radius=Re, color='b')
	ax.add_patch(circ)
	
	plt.scatter(pos[0], pos[1])
	#plt.ylim([-9000000,9000000])
	#plt.xlim([-9000000,9000000])

	#plt.plot(time,alt)
	plt.show()

	m01 = R.mw1 + R.mw2 + R.mp
	m11 = R.md1 + R.mi1 + R.mw2 + R.mp
	m02 = R.mw2 + R.mp
	m12 = R.md2 + R.mi2 + R.mp
	Isp1avg = (R.isp1v + R.isp1sl)/2 								#self.Isp1SL ger en mycket mindre mp
	dVRockeq = ascTime.rockEq(m01, m11, m02, m12, Isp1avg, R.isp2v)
	print "deltaV capability",dVRockeq

	plt.subplot(4,1,1)
	plt.plot(time,altitudes)
	plt.ylabel("altitude [m]")

	plt.subplot(4,1,2)
	plt.plot(time,beta*180/math.pi)
	plt.ylabel("angle to horizon, beta [deg]")

	plt.subplot(4,1,3)
	plt.plot(time,speed)
	plt.ylabel("speed [m/s]")

	plt.subplot(4,1,4)
	drymasstot = np.ones((len(solutions),1))*(3300+182+payload)
	plt.plot(time,mass,time,drymasstot)
	plt.ylabel("mass [kg]")
	plt.xlabel("time [s]")
	plt.show()

	plt.subplot(3,1,1)
	plt.plot(time,apsis[0]-Re)
	plt.ylabel("periapsis-Re [m]")
	plt.subplot(3,1,2)
	plt.plot(time,apsis[1]-Re)
	plt.ylabel("apoapsis-Re [m]")
	plt.subplot(3,1,3)
	plt.plot(time,apsis[2]-Re)
	plt.ylabel("orthdist-Re [m]")
	plt.show()
	
	plt.subplot(2,1,1)
	plt.plot(time, thrust)
	plt.ylabel("thrust [N]")
	plt.subplot(2,1,2)
	plt.plot(time,deltaV)
	plt.ylabel("applied deltaV [m/s]")
	plt.xlabel("time [s]")
	plt.show()
	plt.plot(time, thrust/(mass))
	plt.show()
