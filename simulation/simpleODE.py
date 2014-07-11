import numpy as np
from scipy import integrate
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import scipy.constants as consts
from scipy.integrate import odeint

"""
Basic program to simulate a ballistic trajectory with and without drag.

This could be used as a framework for developing a rocket simulation, by
extending the functions and adding function top simulate thrust, navigation,
etc..

"""

Me = 5.97219e24 			# Earth mass
Re = 6371000				# Earth radius

def projectileDrag(t,w):
	"""
	Function for modelling a projectile motion with drag
	"""

	#Params
	g = consts.g 			# Just g
 	m = 1 					# Mass
	r = 0.1 				# Radius of ball thrown
	A = math.pi*r**2 		# Ball cross section area
	rho = 0 				# Air density
	Cd = 0.25				# Drag coeff. pulled out of nowhere
	beta = 0.5*A*rho*Cd 
	#End params

	Xdot = w[0]
	xdot = w[1]
	Ydot = w[2]
	ydot = w[3]

	V = norm([xdot, ydot])
	grav = gravAcc([Xdot, Ydot])
	return [xdot, -beta/m*V*xdot+grav[0], ydot, -beta/m*V*ydot+grav[1]]

def projectile(w,t):
	""" Projectile motion without drag, for comparisson """
	Xdot = w[0]
	xdot = w[1]
	Ydot = w[2]
	ydot = w[3]
	return [xdot, 0, ydot, -consts.g]

def gravAcc(pos):
	""" Used to calculate the gravity varying with position """
	F = 4*[-consts.G*Me*pos[0]/(norm(pos)**3),
		-consts.G*Me*pos[1]/(norm(pos)**3)]
	return F


if __name__=='__main__':

	t_start = 0.0
	t_final = 10000;
	delta_t = 1;
	numsteps = np.floor((t_final-t_start)/delta_t)+1

	time = [t_final*float(i)/(numsteps) for i in range(int(numsteps))]
 	"""initial params"""
 	x0 = Re			# initial x-position
 	y0 = -100 	 	# initial y-position
 	xdot0 = 600		# initial x-velocity
 	ydot0 = 0		# initial y-position

 	""" Old with odeint"""
 	# sol2 = odeint(projectileDrag, [x0, xdot0, y0, ydot0], time)		# w drag
 	# sol2 = sol2.T

 	"""New with vode"""
  	r = integrate.ode(projectileDrag).set_integrator('vode', method='bdf')
  	r.set_initial_value([x0, xdot0, y0, ydot0], t_start)
  	t = np.zeros((numsteps,1))
  	t[0]=0
  	rx = np.zeros((numsteps,1))
  	ry = np.zeros((numsteps,1))
  	velx = np.zeros((numsteps,1))
  	vely = np.zeros((numsteps,1))
  	i=1
	while r.successful() and i < numsteps:
	 	r.integrate(r.t + delta_t)
	 	t[i] = r.t
	 	rx[i] = r.y[0]
	 	velx[i] = r.y[1]
	 	ry[i] = r.y[2]
	 	vely[i] = r.y[3]
	 	i+=1
	"""End integration """

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	circ=plt.Circle((200,200), Re, color='b', fill=False)
	ax.add_patch(circ)
	plt.show()









