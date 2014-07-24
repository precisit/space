import numpy as np
from scipy.integrate import odeint
import atmofunc
import math
import matplotlib.pyplot as plt
import scipy.constants as consts
import RocketClass
import OrbitCalculations as OC

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
	thrust = rocket.ThrustGravTurn(pos,vel,t)

	"""
	if OC.ApsisCalculation(pos, vel)[0] >= Re+200000 and not rocket.reach:
		rocket.cutFuel = True
		rocket.reach = True
		print OC.ApsisCalculation(pos, vel)-np.array([Re,Re])
		thrust = np.array([0,0,0])
	"""
	#print thrust
	dm = rocket.mcurr-w[6] 						# Mass of the rocket
	dv = np.linalg.norm(thrust)/rocket.mcurr

	GravityAcc = GravAcc(pos) 					# Acceleration due to gravity
	acc = (1/rocket.mcurr)*(-dragForce*velUnit + thrust)+GravityAcc

	return [vel[0], acc[0],
			vel[1], acc[1],
			vel[2], acc[2], dm, dv]

def GravAcc(pos):
	""" Calculates the gravitational acceleration at the current position """
	return -pos*consts.G*Me/(np.linalg.norm(pos)**3)

"""
Test program
"""
if __name__ == '__main__':
	"""Initial conditions """
	lat = math.radians(0) 									# Latitude
	longi = math.radians(90)								# Longitude
	initPos = Re*np.array([math.cos(lat)*math.cos(longi),
						   math.cos(lat)*math.sin(longi),
						   math.sin(lat)])					# Initial position vector
	initVel = np.cross(We, initPos)							# Initial velocity vector
	print initPos
	initial_conds = [initPos[0], initVel[0], initPos[1], initVel[1], initPos[2], initVel[2],
					 402000+16000+3900+3200+182+90720, 0]
	time = np.linspace(0,30000,1000) 	
	"""
	Rocket initial conditions
	"""
	R = RocketClass.Rocket(402000., 16000., 3900., 320., 280., 5885.e3, 90720., 3200., 182., 345., 800000., 14000., time[0], 25000., 3)

	""" End initial conditions """

						# Time vector to integrator

	solutions = odeint(RocketFunc, initial_conds, time, args=(R,))		# Integrate

	pos = np.array([solutions[:,0], solutions[:,2], solutions[:,4]])
	vel = np.array([solutions[:,1], solutions[:,3], solutions[:,5]])

	mass = solutions[:,6]
	deltaV = solutions[:,7]

	altitudes = np.zeros((len(solutions),1))
	speed = np.zeros((len(solutions),1))
	tang = np.zeros((3,len(solutions)))
	beta = np.zeros((len(solutions),1))
	apsis = np.zeros((3,len(solutions)))

	for i in range(len(solutions)-1):
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
	print max(deltaV)
	#plt.ylim([-9000000,9000000])
	#plt.xlim([-9000000,9000000])

	#plt.plot(time,alt)
	plt.show()

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
	drymasstot = np.ones((len(solutions),1))*(3300+182+14000)
	plt.plot(time,mass,time,drymasstot)
	plt.ylabel("mass [kg]")
	plt.xlabel("time [s]")
	plt.show()

	plt.subplot(3,1,1)
	plt.plot(time,apsis[0]-Re)
	plt.subplot(3,1,2)
	plt.plot(time,apsis[1]-Re)
	plt.subplot(3,1,3)
	plt.plot(time,apsis[2]-Re)
	plt.show()
	print OC.ApsisCalculation(np.array([0,Re+200000.,0]),np.array([7788,0,0]))
	print np.linalg.norm(np.array([0, Re+200000.,0]))
	print Re
	print np.array([0,Re+200000.,0])