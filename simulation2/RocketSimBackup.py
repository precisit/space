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
We = np.array([0,0,2*np.pi/(24*60*60)])
"""
Functions
"""

def RocketFunc(w, t, rocket):
	pos = np.array([w[0], w[2], w[4]])			# Positions
	vel = np.array([w[1], w[3], w[5]]) 			# Velocities
	velUnit = atmofunc.unit(vel)			# Unit velocity vector
	dragForce = atmofunc.dragForce(vel, pos, t)	# Drag force magnitude
	rocket.MainController(t)
	thrust = rocket.newThrustGravTurn(pos,vel,t,w[8])

	dm = rocket.mcurr-w[6] 						# Mass of the rocket
	dv = np.linalg.norm(thrust)/rocket.mcurr
	dT = np.linalg.norm(thrust)-w[8]
	GravityAcc = GravAcc(pos) 					# Acceleration due to gravity
	surfVel = atmofunc.inertToSurfVel(vel,pos,t)
	surfVelUnit = atmofunc.unit(surfVel)
	dragUnit = atmofunc.surfToInertPos(-surfVelUnit,t)
	
	
	acc = (1/rocket.mcurr)*(-dragForce*dragUnit + thrust)+GravityAcc

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
	payload = 10000.
	initial_conds = [initPos[0], initVel[0], initPos[1], initVel[1], initPos[2], initVel[2],
					 402000+90720+payload, 0, 5885.e3]
	timeUncut = np.linspace(0,1000,150000) 	
	"""
	Rocket initial conditions
	"""
	R = RocketClass.Rocket(402000., 16000., 3900., 320., 280., 5885.e3, 90720., 3200., 182., 345., 800000., payload, timeUncut[0], 10000., 25,100)

	""" End initial conditions """


"""
	solutionUncut = odeint(RocketFunc, initial_conds, timeUncut, args=(R,))		# Integrate
	time = timeUncut[0::100]
	solutions = solutionUncut[0::100,:] 
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
	posEarth = np.zeros((3,len(solutions)))
	surfVel = np.zeros((3,len(solutions)))
	surfVelUnit = np.zeros((3,len(solutions)))
	dragUnit = np.zeros((3,len(solutions)))
"""
	pos = np.zeros((3, numsteps))
	vel = np.zeros((3, numsteps))
	mass = np.zeros((numsteps,1))
	deltaV = np.zeros((numsteps,1))
	thrust = np.zeros((numsteps,1))
	transPos = np.zeros((2,numsteps))
	speed = np.zeros((numsteps,1))
	tang = np.zeros((3,numsteps))
	altitudes = np.zeros((numsteps,1))
	beta = np.zeros((numsteps,1))
	posEarth = np.zeros((3,len(solutions)))
	surfVel = np.zeros((3,len(solutions)))
	surfVelUnit = np.zeros((3,len(solutions)))
	dragUnit = np.zeros((3,len(solutions)))
	apsis = np.zeros((3,numsteps))

	while r.successful() and i < numsteps:
		r.integrate(r.t + delta_t)
		t[i] = r.t

		pos[:,i] = np.array([r.y[0], r.y[2], r.y[4]])
		vel[:,i] = np.array([r.y[1], r.y[3], r.y[5]])
		r.set_f_params(R)
		mass[i] = r.y[6]
		deltaV[i] = r.y[7]
		thrust[i] = r.y[8]
		transPos[0,i] = pos[0,i]*np.cos(-We[2]*r.t) - pos[1,i]*np.sin(-We[2]*r.t)
		transPos[1,i] = pos[0,i]*np.sin(-We[2]*r.t) + pos[1,i]*np.cos(-We[2]*r.t)
		speed[i] = np.linalg.norm(vel[:,i])
		tang[:,i] = np.cross(pos[:,i],np.cross(vel[:,i],pos[:,i]))
		altitudes[i] = np.linalg.norm(pos[:,i])-Re
		apsis[:,i] = OC.ApsisCalculation(pos[:,i],vel[:,i])
		beta[i] = OC.angleVec(vel[:,i]-np.cross(We, pos[:,i]),tang[:,i])
		posEarth[0,i] = pos[0,i]*np.cos(-We[2]*time[i]) - pos[1,i]*np.sin(-We[2]*time[i])
		posEarth[1,i] = pos[0,i]*np.sin(-We[2]*time[i]) + pos[1,i]*np.cos(-We[2]*time[i])

		surfVel[:,i] = atmofunc.inertToSurfVel(vel[:,i],pos[:,i],time[i])
		surfVelUnit[:,i] = atmofunc.unit(surfVel[:,i])
		dragUnit[:,i] = atmofunc.surfToInertPos(-surfVelUnit[:,i],time[i])

		i+=1
"""
	for i in range(len(solutions)):
		altitudes[i] = np.linalg.norm(pos[:,i])-Re
		speed[i] = np.linalg.norm(vel[:,i])
		tang[:,i] = np.cross(pos[:,i],np.cross(vel[:,i],pos[:,i]))
		if (not np.linalg.norm(tang)==0):
			beta[i] = OC.angleVec(vel[:,i],tang[:,i])
		apsis[:,i] = OC.ApsisCalculation(pos[:,i],vel[:,i])
		posEarth[0,i] = pos[0,i]*np.cos(-We[2]*time[i]) - pos[1,i]*np.sin(-We[2]*time[i])
		posEarth[1,i] = pos[0,i]*np.sin(-We[2]*time[i]) + pos[1,i]*np.cos(-We[2]*time[i])

		surfVel[:,i] = atmofunc.inertToSurfVel(vel[:,i],pos[:,i],time[i])
		surfVelUnit[:,i] = atmofunc.unit(surfVel[:,i])
		dragUnit[:,i] = atmofunc.surfToInertPos(-surfVelUnit[:,i],time[i])
"""
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
	plt.plot(time, thrust/(mass*consts.g))
	plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ = plt.Circle((0,0), radius=Re, color='b')
	ax.add_patch(circ)
	plt.quiver(pos[0], pos[1],tang[0],tang[1])
	plt.show()