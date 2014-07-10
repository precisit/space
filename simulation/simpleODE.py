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

def projectileDrag(w,t):

	"""
	Function for modelling a projectile motion with drag
	"""

	#Params
	g = consts.g 			# Just g
 	m = 1 					# Mass
	r = 0.1 				# Radius of ball thrown
	A = math.pi*r**2 		# Ball cross section area
	rho = 1.225 			# Air density
	Cd = 0.25				# Drag coeff. pulled out of nowhere
	beta = 0.5*A*rho*Cd 
	#End params

	Xdot = w[0]
	xdot = w[1]
	Ydot = w[2]
	ydot = w[3]

	V = norm([xdot, ydot])
	return [xdot, -beta/m*V*xdot, ydot, -beta/m*V*ydot-consts.g]

def projectile(w,t):

	Xdot = w[0]
	xdot = w[1]
	Ydot = w[2]
	ydot = w[3]

	return [xdot, 0, ydot, -consts.g]

def fun(y,t):
	Ydot = y[0]
	ydot = y[1]
	return [ydot, -consts.g]
	

if __name__=='__main__':

	t_start = 0.0
	t_final = 10;
	delta_t = 0.01;
	numsteps = np.floor((t_final-t_start)/delta_t)

	time = [t_final*float(i)/(numsteps) for i in range(int(numsteps))]
 	"""initial params"""
 	x0 = 0 			# initial x-position
 	y0 = 0 			# initial y-position
 	xdot0 = 0		# initial x-velocity
 	ydot0 = 100		# initial y-position

 	sol1 = odeint(projectile, [x0, xdot0, y0, ydot0], time) 		# w/o drag
 	sol1 = sol1.T
 	sol2 = odeint(projectileDrag, [x0, xdot0, y0, ydot0], time)		# w drag
 	sol2 = sol2.T

	plt.plot(time, sol1[2], time, sol2[2])
	plt.show()









