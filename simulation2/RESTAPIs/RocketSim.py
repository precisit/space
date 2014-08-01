import numpy as np
from scipy import integrate
import atmofunc
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

def RocketFunc(t, w, rocket):
	pos = np.array([w[0], w[2], w[4]])			# Positions
	vel = np.array([w[1], w[3], w[5]]) 			# Velocities
	velUnit = atmofunc.unit(vel)			# Unit velocity vector
	
	dragForce = atmofunc.dragForce(vel, pos)	# Drag force magnitude
	rocket.MainController(t)
	thrust = rocket.thrustGravTurn(pos, vel, t ,w[8])

	dm = rocket.mcurr-w[6] 						# Mass of the rocket
	dv = np.linalg.norm(thrust)/rocket.mcurr
	dT = np.linalg.norm(thrust)-w[8]
	
	GravityAcc = GravAcc(pos) 					# Acceleration due to gravity
	
	dragUnit = atmofunc.unit(atmofunc.inertToSurfVel(vel,pos))
		
	acc = (1/rocket.mcurr)*(-dragForce*dragUnit + thrust)+GravityAcc

	return [vel[0], acc[0],
			vel[1], acc[1],
			vel[2], acc[2], dm, dv, dT]

def GravAcc(pos):
	""" Calculates the gravitational acceleration at the current position """
	return -pos*consts.G*Me/(np.linalg.norm(pos)**3)

"""
Gor sa att pitchAlt, initialPitch och gmax satts i rocket-objektet
"""
def RocketSimulator(rocket, long, lat, alt, tmax, dt, optional):
	t_start = 0.0
	t_final = tmax
	delta_t = dt
	numsteps = np.floor((t_final-t_start)/delta_t)+1
	t = np.zeros((numsteps,1))
	t[0] = 0

	at = np.radians(0) 									# Latitude
	longi = np.radians(273)								# Longitude
	initPos = Re*np.array([np.cos(lat)*np.cos(long),
				 np.cos(lat)*np.sin(long),
				 np.sin(lat)])							# Initial position vector
	initVel = np.cross(We, initPos)						# Initial velocity vector

	initial_conds = [initPos[0], initVel[0], initPos[1], initVel[1], initPos[2], initVel[2],
					 rocket.mcurr, 0, 5885.e3]

	r = integrate.ode(RocketFunc).set_integrator('vode', method='bdf')
	r.set_initial_value(initial_conds, t_start).set_f_params(rocket)

	pos = np.zeros((3, numsteps))
	vel = np.zeros((3, numsteps))
	deltaV = np.zeros((numsteps,1))
	
	draglosses = 0
	gravlosses = 0
	thrust = np.array([0])
	drag = np.array([0])
	pitchangle = np.array([0])
	
	if optional['draglosses']:
		print 'Draglosses'
	if optional['gravlosses']:
		print 'Gravlosses'
	if optional['thrust']:
		thrust = np.zeros((numsteps,1))
	if optional['drag']:
		drag = np.zeros((3,numsteps))
	if optional['pitchangle']:
		print 'Pitchangle'

	i=1
	while r.successful() and i < numsteps:
		r.integrate(r.t + delta_t)
		t[i] = r.t
		pos[:,i] = np.array([r.y[0], r.y[2], r.y[4]])
		vel[:,i] = np.array([r.y[1], r.y[3], r.y[5]])
		deltaV[i] = r.y[7]

		if optional['draglosses']:
			print 'Draglosses'
		if optional['gravlosses']:
			print 'Gravlosses'
		if optional['thrust']:
			thrust[i] = r.y[8]
		if optional['pitchangle']:
			print 'Pitchangle'
		if optional['drag']:
			drag[i] = vel[:,i]-np.cross(We,pos[:,i])
		r.set_f_params(rocket)
		i+=1
	return pos.tolist(), vel.tolist(), np.max(deltaV), draglosses, gravlosses, thrust.tolist(), drag.tolist(), pitchangle.tolist()


"""
Test program
"""
if __name__ == '__main__':
	startTime = timer.time()
	"""Initial conditions """
	lat = np.radians(0) 									# Latitude
	longi = np.radians(273)								# Longitude
	initPos = Re*np.array([np.cos(lat)*np.cos(longi),
						   np.cos(lat)*np.sin(longi),
						   np.sin(lat)])					# Initial position vector
	initVel = np.cross(We, initPos)							# Initial velocity vector
	payload = 13000.
	initial_conds = [initPos[0], initVel[0], initPos[1], initVel[1], initPos[2], initVel[2],
					 402000+90720+payload, 0, 5885.e3]
	t_start = 0.0
	t_final = 8000
	delta_t = 2
	numsteps = np.floor((t_final-t_start)/delta_t)+1 	
	t = np.zeros((numsteps,1))
	t[0] = 0

	"""
	Rocket initial conditions
	"""
	R = RocketClass.Rocket(402000., 16000., 3900., 320., 280., 5885.e3, 90720., 3200., 182., 345., 800000., payload, t[0], 10000, 2.5,100)
	r = integrate.ode(RocketFunc).set_integrator('vode', method='bdf')
	r.set_initial_value(initial_conds, t_start).set_f_params(R)
	

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
	posEarth = np.zeros((3,numsteps))
	surfVel = np.zeros((3,numsteps))
	surfVelUnit = np.zeros((3,numsteps))
	dragUnit = np.zeros((3,numsteps))
	apsis = np.zeros((3,numsteps))
	i=1
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
		posEarth[0,i] = pos[0,i]*np.cos(-We[2]*t[i]) - pos[1,i]*np.sin(-We[2]*t[i])
		posEarth[1,i] = pos[0,i]*np.sin(-We[2]*t[i]) + pos[1,i]*np.cos(-We[2]*t[i])

		surfVel[:,i] = atmofunc.inertToSurfVel(vel[:,i],pos[:,i])
		surfVelUnit[:,i] = atmofunc.unit(surfVel[:,i])
		dragUnit[:,i] = (vel[:,i]-np.cross(We,pos[:,i]))/np.linalg.norm(vel[:,i]-np.cross(We,pos[:,i]))#atmofunc.surfToInertPos(-surfVelUnit[:,i],t[i])

		i+=1

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ = plt.Circle((0,0), radius=Re, color='b')
	ax.add_patch(circ)
	
	plt.quiver(pos[0], pos[1], dragUnit[0], dragUnit[1])
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
	plt.plot(t,altitudes)
	plt.ylabel("altitude [m]")
	plt.subplot(4,1,2)
	plt.plot(t,beta*180/np.pi)
	plt.ylabel("angle to horizon, beta [deg]")

	plt.subplot(4,1,3)
	plt.plot(t,speed)
	plt.ylabel("speed [m/s]")

	plt.subplot(4,1,4)
	drymasstot = np.ones((numsteps,1))*(3300+182+payload)
	plt.plot(t,mass,t,drymasstot)
	plt.ylabel("mass [kg]")
	plt.xlabel("time [s]")
	plt.show()

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
	
	plt.subplot(2,1,1)
	plt.plot(t, thrust)
	plt.ylabel("thrust [N]")
	plt.subplot(2,1,2)
	plt.plot(t,deltaV)
	plt.ylabel("applied deltaV [m/s]")
	plt.xlabel("time [s]")
	plt.show()
	plt.plot(t, thrust/(mass*consts.g))
	plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ = plt.Circle((0,0), radius=Re, color='b')
	ax.add_patch(circ)
	plt.quiver(transPos[0], transPos[1],tang[0],tang[1])
	plt.show()