import numpy as np
from scipy.integrate import odeint
import atmofunc
import math
import matplotlib.pyplot as plt
import scipy.constants as consts
import RocketClass

# Earth constants
Me = 5.97219e24
Re = 6371000
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

	thrust = atmofunc.thrustEff(rocket.isp, rocket.Ae1, pos, rocket.mdot)


	dm = rocket.mcurr-w[6] 						# Mass of the rocket
	dv = thrust/rocket.mcurr


	GravityAcc = GravAcc(pos) 					# Acceleration due to gravity
	acc = (1/rocket.mcurr)*(-dragForce*velUnit + thrust*initPos/np.linalg.norm(initPos))+GravityAcc

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
	time = np.linspace(0,1000,10000) 	
	"""
	Rocket initial conditions
	"""
	R = RocketClass.Rocket(402000, 16000, 3900, 320, 280, 5885e3, 90720, 3200, 182, 345, 800000, 14000,time[0])

	""" End initial conditions """

						# Time vector to integrator

	solutions = odeint(RocketFunc, initial_conds, time, args=(R,))		# Integrate

	pos = np.array([solutions[:,0], solutions[:,2], solutions[:,4]])
	vel = np.array([solutions[:,1], solutions[:,3], solutions[:,5]])

	mass = solutions[:,6]
	deltaV = solutions[:,7]

	altitudes = np.zeros((len(solutions),1))
	speed = np.zeros((len(solutions),1))
	
	for i in range(len(solutions)-1):
		altitudes[i] = np.linalg.norm(pos)
		speed[i] = np.linalg.norm(vel[:,i])
	"""
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ = plt.Circle((0,0), radius=Re, color='b')
	ax.add_patch(circ)
	"""

	plt.plot(time,vel[0,:])
	print max(deltaV)
	#plt.ylim([-9000000,9000000])
	#plt.xlim([-9000000,9000000])

	#plt.plot(time,alt)
	plt.show()