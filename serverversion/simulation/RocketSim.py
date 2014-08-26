import numpy as np
from scipy import integrate
import atmofunc
#import matplotlib.pyplot as plt
import scipy.constants as consts
import RocketClass3stage
import OrbitCalculations as OC
#import time as timer
import ascTime
# Earth constants
Me = 5.97219e24
Re = 6371000.
We = np.array([0,0,2*np.pi/(24*60*60)])
"""
Functions
"""

def RocketFunc(t, w, rocket):
	""" This is the function that governs the movement equations of the rocket. """

	pos = np.array([w[0], w[2], w[4]])			# Positions
	vel = np.array([w[1], w[3], w[5]]) 			# Velocities
	velUnit = atmofunc.unit(vel)				# Unit velocity vector

	dragForce = atmofunc.dragForce(vel, pos, rocket.Aflow)	# Drag force magnitude
	rocket.MainController(t)

	thrust = rocket.thrustGravTurn(pos, vel, t, w[8])
	#thrust = rocket.ThrustAlgorithm(pos,vel)

	GravityAcc = GravAcc(pos) 					# Acceleration due to gravity
	dm = rocket.mcurr-w[6] 						# Mass of the rocket
	dv = np.linalg.norm(thrust)/rocket.mcurr 	# Delta-V
	dT = np.linalg.norm(thrust)-w[8] 			# Thrust
	dDrag = np.linalg.norm(dragForce)-w[9]#/rocket.mcurr # Draglosses

	horizon = OC.GetHorizontalUnitVector(pos, vel)
	horizonAng = OC.AngleBetweenVectors(horizon, thrust)
	dGravdrag = (np.linalg.norm(GravityAcc))*np.sin(horizonAng) 
	
	dragUnit = atmofunc.unit(atmofunc.inertToSurfVel(vel,pos))

	acc = (1/rocket.mcurr)*(-dragForce*dragUnit + thrust)+GravityAcc # Resulting acceleration for the rocket

	return [vel[0], acc[0],
			vel[1], acc[1],
			vel[2], acc[2], dm, dv, dT, dDrag, dGravdrag]

def GravAcc(pos):
	""" Calculates the gravitational acceleration at the current position """
	return -pos*consts.G*Me/(np.linalg.norm(pos)**3)

"""
Gor sa att pitchAlt, initialPitch och gmax satts i rocket-objektet
"""
def RocketSimulator(rocket, longi, lat, tmax, dt, optional):
	t_start = 0.0
	t_final = tmax
	delta_t = dt
	numsteps = np.floor((t_final-t_start)/delta_t)+1
	t = np.zeros((numsteps,1))
	t[0] = 0

	lat = np.radians(lat) 									# Latitude
	longi = np.radians(longi)								# Longitude
	initPos = Re*np.array([np.cos(lat)*np.cos(longi),
				 np.cos(lat)*np.sin(longi),
				 np.sin(lat)])								# Initial position vector
	initVel = np.cross(We, initPos)							# Initial velocity vector

	initial_conds = [initPos[0], initVel[0], initPos[1], initVel[1], initPos[2], initVel[2],
					 rocket.mcurr, 0, rocket.thr1sl,0,0]

	r = integrate.ode(RocketFunc).set_integrator('vode', method='bdf')
	r.set_initial_value(initial_conds, t_start).set_f_params(rocket)

	pos = np.zeros((3, numsteps))
	vel = np.zeros((3, numsteps))
	deltaV = np.zeros((numsteps,1))
	mass = np.zeros((numsteps,1))

	draglosses = 0
	gravlosses = 0
	thrust = np.array([0])
	drag = np.array([0])
	downrange = np.array([0])

	if optional['draglosses']:
		draglosses = np.zeros((numsteps, 1))
	if optional['gravlosses']:
		gravlosses = np.zeros((numsteps, 1))
	if optional['thrust']:
		thrust = np.zeros((numsteps,1))
	if optional['drag']:
		drag = np.zeros((numsteps,1))
	if optional['downrange']:
		downrange = np.zeros((numsteps, 1))

	i=0
	while r.successful() and i < numsteps:
		r.integrate(r.t + delta_t)
		t[i] = r.t
		pos[:,i] = np.array([r.y[0], r.y[2], r.y[4]])
		vel[:,i] = np.array([r.y[1], r.y[3], r.y[5]])
		deltaV[i] = r.y[7]
		mass[i] = r.y[6]

		if optional['draglosses'] and not i == 0:
			draglosses[i] = draglosses[i-1] + delta_t*(r.y[9]+drag[i-1])/(r.y[6]+mass[i-1]) 
		if optional['gravlosses']:
			gravlosses[i] = r.y[10]
		if optional['thrust']:
			thrust[i] = r.y[8]
		if optional['downrange'] and not i == 0:
			downrange[i] = OC.DownRangeDist(pos[:,i-1], pos[:,i], t[i]) + downrange[i-1]
		if optional['drag']:
			drag[i] = r.y[9]
		r.set_f_params(rocket)
		if np.linalg.norm(pos[:,i])-Re<-1: 
			break
		i+=1
	return pos[:,:i].tolist(), vel[:,:i].tolist(), t[:i].tolist(), mass[:i].tolist(), np.max(deltaV), np.max(draglosses), np.max(gravlosses), thrust[:i].tolist(), drag[:i].tolist(), downrange[:i].tolist()


"""
Test program
"""
if __name__ == '__main__':
	startTime = timer.time()
	"""Initial conditions """
	lat = np.radians(0) 									# Latitude
	longi = np.radians(90)									# Longitude
	initPos = Re*np.array([np.cos(lat)*np.cos(longi),
						   np.cos(lat)*np.sin(longi),
						   np.sin(lat)])					# Initial position vector

	initVel = np.cross(We, initPos)							# Initial velocity vector

#	payload = 18000.
	
	t_start = 0.0
	t_final = 4000
	delta_t = 1
	numsteps = np.floor((t_final-t_start)/delta_t)+1 	
	t = np.zeros((numsteps,1))
	t[0] = 0

	"""
	Rocket initial conditions
	"""
	R = RocketClass3stage.CreateRocket({'type':'saturnv', 'payload':10000, 'lat':0, 'tAlt':200000, 'gmax':1000,
								'optional':{'draglosses':True, 'thrust':True, 'gravlosses':True, 'downrange':True}, 
								'tmax':8000 , 'gAlt':20000, 'gT':10, 'initAng':4, 'gAng':45})
	"""
	R = RocketClass3stage.Rocket(10.e3, 0, 10.e3, 2.6, 500., 200e3,
						402000., 16000., 3900., 320., 280., 5885.e3, 21.237,
						90720., 3200., 182., 345, 800e3)
		
	"""
	"""
	R = RocketClass3stage.Rocket(payload, t[0], 2000000, 2.5,100,
							1.79e5, 1.27e4, 0, 430, 340, 1.11e6,
						   	1.25e4, 2.7e3,  0, 324, 2.24e4,
						  	555000, 79600, 0, 275, 6.47e6, True) #Ariane 5
	"""
	"""
	R = RocketClass3stage.Rocket(payload, t[0], 10000, 4, 5, 300000,
							2286217, 135218, 0, 304, 265, 38703000,
							490778, 39048, 0, 421, 5.17e6,
							119900, 13300, 0, 421, 1.03e6, False)
	"""
	initial_conds = [initPos[0], initVel[0], initPos[1], initVel[1], initPos[2], initVel[2],
					 R.mw1+R.mw2+R.mw3+R.mp, 0, R.thr1sl,0,0]
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
	draglosses = np.zeros((numsteps,1))
	gravlosses = np.zeros((numsteps,1))
	i=0
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
		beta[i] = OC.AngleBetweenVectors(vel[:,i]-np.cross(We, pos[:,i]),tang[:,i])
		posEarth[0,i] = pos[0,i]*np.cos(-We[2]*t[i]) - pos[1,i]*np.sin(-We[2]*t[i])
		posEarth[1,i] = pos[0,i]*np.sin(-We[2]*t[i]) + pos[1,i]*np.cos(-We[2]*t[i])

		surfVel[:,i] = atmofunc.inertToSurfVel(vel[:,i],pos[:,i])
		surfVelUnit[:,i] = atmofunc.unit(surfVel[:,i])
		dragUnit[:,i] = (vel[:,i]-np.cross(We,pos[:,i]))/np.linalg.norm(vel[:,i]-np.cross(We,pos[:,i]))#atmofunc.surfToInertPos(-surfVelUnit[:,i],t[i])
		draglosses[i] = r.y[9]
		gravlosses[i] = r.y[10]
		i+=1
	
	
	print "Total delta-V",deltaV[len(deltaV)-1]
	print "Draglosses: ", draglosses[len(draglosses)-1]
	print "gravlosses: ", gravlosses[len(gravlosses)-1]
	
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ = plt.Circle((0,0), radius=Re, color='b')
	ax.add_patch(circ)
	
	plt.plot(pos[0], pos[1])
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
	drymasstot = np.ones((numsteps,1))*(R.md3+R.mi3+R.mp)
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
	plt.plot(t, draglosses)
	plt.ylabel("Draglosses ")
	plt.xlabel("time [s]")
	plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ = plt.Circle((0,0), radius=Re, color='b')
	ax.add_patch(circ)
	plt.quiver(transPos[0], transPos[1],tang[0],tang[1])
	plt.show()

	plt.plot(t, gravlosses)
	plt.show()
 
