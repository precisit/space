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

Me = 5.97219e24 				# Earth mass [kg]
Re = 6371000					# Earth radius [m]
We = 2*math.pi/(24*60*60)		# Earth rotational velocity

def projectileDrag(t,w):
	"""
	Function for modelling a projectile motion with thrust, variable mass and drag.

	When this program gets RESTified, we probably should send the parameters below as 
	input arguments.
	"""

	# Physical params
	g = consts.g 			# Just g [m/s^2]
	rho = 0.3 				# Air density [kg/m^3]
	Cd = 0.25				# Drag coeff. pulled out of nowhere
	
	Mwet = 500000			# Total rocket mass (wet mass) [kg]
	Mfuel = 470000			# Fuel mass	[kg]
	Isp = 340				# Specific impulse
	Thr = 5885e3			# Thrust [N]
	mdot = Thr/(Isp*g)		# Fuel burn rate [kg/s]
	angle = (-0.35*t+90)*math.pi/180 	# Thrust angle - temporary

	#Launch params
	latDeg = 28					# Launch latitude in degrees
	lat = latDeg*math.pi/180	# Degrees to radians
	initV = We*Re*cos(lat)		# Initial velocity contribution due to earth rotation
	"""
	mdot = 100				# Fuel burn rate [kg/s]
	Vex = 5500  			# Exhaus velocity of burnt fuel [m/s]
	"""
	#End params

	Xdot = w[0] 			# x-pos
	xdot = w[1]				# x-vel
	Ydot = w[2]				# y-pos
	ydot = w[3]				# y-vel
	Zdot = w[4]				# z-pos
	zdot = w[5]				# z-vel
	v = np.array([xdot, ydot, zdot])
	pos = np.array([Xdot,Ydot,Zdot])
	Mburnt = mdot*t							# burnt fuel fuel mass at time t [kg]
 	Mcurr = Mwet-Mburnt	 					# Current mass
 	# If no fuel left, cut mdot
	if Mburnt >= Mfuel:#
		mdot = 0
		Mcurr = Mwet-Mfuel

	V = norm(v)										# Absolute value of the velocity
	altitude = norm([Xdot, Ydot, Zdot]) 		# Altitude
	dragF = atmofunc.dragForce(V, pos)		# Magnitude of the drag force
	Vunit = [xdot/V, ydot/V, zdot/V]			# Unit velocity vector
	grav = gravAcc([Xdot, Ydot, Zdot]) 			# Gravitational acceleration

	return [xdot, (1/Mcurr)*(-dragF*Vunit[0]+Thr*math.cos(angle))-grav[0],
			ydot, (1/Mcurr)*(-dragF*Vunit[1]+Thr*math.sin(angle))-grav[1],
			Zdot, (1/Mcurr)*(-dragF*Vunit[2]+0*Thr*Vunit[2])-grav[2]]

def gravAcc(pos):
	""" Used to calculate the gravity, varying with position """
	F = 4*[consts.G*Me*pos[0]/(norm(pos)**3),
		consts.G*Me*pos[1]/(norm(pos)**3),
		consts.G*Me*pos[2]/(norm(pos)**3)]
	return F

if __name__=='__main__':

	"""Time parameters"""
	t_start = 0.0
	t_final = 100000;
	delta_t =2;
	numsteps = np.floor((t_final-t_start)/delta_t)+1

 	"""initial params"""
 	x0 = 0 				# initial x-position
 	y0 = Re  			# initial y-position
 	z0 = 0 				# initial z-position
 	xdot0 = 1			#initial x-velocity
 	ydot0 =1			#initial y-velocity
 	zdot0 = 0			#initial z-velocity
 	initial_conds = [x0, xdot0, y0, ydot0, z0, zdot0]

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
	for i in range(len(t)):
		velocity[i] = sqrt(velx[i]**2+vely[i]**2+velz[i]**2)
	"""End integration """

	"""Plotting 3D
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
	plt.show()




