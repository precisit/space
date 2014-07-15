import numpy as np
from scipy import integrate
from matplotlib.pylab import *
from matplotlib import animation
import matplotlib.pyplot as plt
import scipy.constants as consts
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
import atmofunc

"""
This is supposed to be an extension of simpleODE, with more forces and function added
to the rocket, such as thrust, thrust vectoring, mass loss, varying air density etc..

"""

Me = 5.97219e24 								# Earth mass [kg]
Re = 6371000									# Earth radius [m]
We = np.array([0,0,2*math.pi/(24*60*60)])		# Earth rotational velocity vector

def projectileDrag(t,w):
	"""
	Function for modelling a projectile motion with thrust, variable mass and drag.

	When this program gets RESTified, we probably should send the parameters below as 
	input arguments.
	"""
	
	# Rocket parameters
	Mwet = 500000				# Total rocket mass (wet mass) [kg]
	Mfuel = 470000				# Fuel mass	[kg]
	Isp = 400					# Specific impulse
	Thr = 5885e3				# Thrust [N]
	mdot = Thr/(Isp*consts.g)		# Fuel burn rate [kg/s]
	angle = (+0.3*t+90)*math.pi/180 	# Thrust angle - temporary

	"""
	mdot = 100				# Fuel burn rate [kg/s]
	Vex = 5500  			# Exhaus velocity of burnt fuel [m/s]
	"""
	#End params

	positions = np.array([w[0], w[2], w[4]]) 				# Positions
	velocities = np.array([w[1], w[3], w[5]]) 	# Velocities

	Vunit = velocities/norm(velocities) 									# Unit velocity vector

	Mburnt = mdot*t							# burnt fuel fuel mass at time t [kg]
 	Mcurr = Mwet-Mburnt	 					# Current mass
 	# If no fuel left, cut mdot
	if Mburnt >= Mfuel:
		mdot = 0
		Mcurr = Mwet-Mfuel

	dragF = atmofunc.dragForce(velocities, positions)	# Magnitude of the drag force
	grav = gravAcc(positions) 							# Gravitational acceleration
	
	return [velocities[0], (1/Mcurr)*(-dragF*Vunit[0]+Thr*math.cos(angle))-grav[0],
			velocities[1], (1/Mcurr)*(-dragF*Vunit[1]+Thr*math.sin(angle))-grav[1],
			velocities[2], (1/Mcurr)*(-dragF*Vunit[2]+0*Thr*Vunit[2])-grav[2]]

def gravAcc(pos):
	""" Used to calculate the gravity, varying with position """
	F = pos*consts.G*Me/(norm(pos)**3)
	return F

if __name__=='__main__':

	"""Time parameters"""
	t_start = 0.0
	t_final = 10000;
	delta_t =1;
	numsteps = np.floor((t_final-t_start)/delta_t)+1

 	"""initial params"""

	#Initial launch params
	latDeg = 0					# Launch latitude in degrees
	longDeg = 90 					# Longitude
	lat = latDeg*math.pi/180		# Degrees to radians
	longi = longDeg*math.pi/180		# Radians

	initR = Re*np.array([math.cos(longi)*math.cos(lat), 
			math.sin(longi)*math.cos(lat),
	 		math.sin(lat)]) 		# Initial position vector
	initV = np.cross(We, initR)		# Initial velocity contribution due to earth rotation

 	initial_conds = [initR[0], initV[0], initR[1], initV[1], initR[2], initV[2]] # Initial condition to solver

 	"""Solve with odeint"""
 	#time = [t_final*float(i)/(numsteps) for i in range(int(numsteps))]
 	# sol2 = odeint(projectileDrag, [x0, xdot0, y0, ydot0], time)		# w drag
 	# sol2 = sol2.T

 	"""Solve with VODE"""
  	r = integrate.ode(projectileDrag).set_integrator('vode', method='bdf')
  	r.set_initial_value(initial_conds, t_start)
  	t = np.zeros((numsteps,1))

  	t[0]=0

  	rx = np.zeros((numsteps,1))
  	ry = np.zeros((numsteps,1))
  	rz = np.zeros((numsteps,1))
  	velx = np.zeros((numsteps,1))
  	vely = np.zeros((numsteps,1))
  	velz = np.zeros((numsteps,1))

  	i=1

	while r.successful() and i < numsteps:
	 	r.integrate(r.t + delta_t)
	 	t[i] = r.t

	 	rx[i] 	= r.y[0]
	 	velx[i] = r.y[1]

	 	ry[i] 	= r.y[2]
	 	vely[i] = r.y[3]

	 	rz[i] 	= r.y[4]
	 	velz[i] = r.y[5]
	 	
	 	if norm([rx[i], ry[i], rz[i]])-Re < 0:
	 		break
	 	
	 	i+=1

	velocity = np.zeros((numsteps,1))
	altitude = np.zeros((numsteps,1))
	for i in range(len(t)):
		velocity[i] = sqrt(velx[i]**2+vely[i]**2+velz[i]**2)
		altitude[i] = sqrt(rx[i]**2+ry[i]**2+rz[i]**2)-Re
	"""End integration """

	"""Plotting 3D"""
	"""
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(rx,ry,rz, marker='.')
	
	#Plot earth-size sphere
	
	phi = np.linspace(0, 2 * np.pi, 100)
	theta = np.linspace(0, np.pi, 100)
	xm = Re * np.outer(np.cos(phi), np.sin(theta))
	ym = Re * np.outer(np.sin(phi), np.sin(theta))
	zm = Re * np.outer(np.ones(np.size(phi)), np.cos(theta))
	ax.plot_surface(xm, ym, zm)
	ax.set_xlabel('X-axis')
	ax.set_ylabel('Y-axis')
	ax.set_zlabel('Z-axis')

	fig2 = plt.figure()
	ax2 = fig2.add_subplot(1,1,1)
	ax2.plot(t, velocity, t, altitude)
	plt.show()
	"""

	""" Plotting 2D"""
	
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ = plt.Circle((0,0), radius=Re, color='b')
	ax.add_patch(circ)
	plt.scatter(rx,ry, marker='.',color='black', s=10)
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(1,1,1)
	ax2.plot(t, velocity)
	ax2.set_xlabel('X-axis')
	ax2.set_ylabel('Y-axis')
	plt.show()
	



