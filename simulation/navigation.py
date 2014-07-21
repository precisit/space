import scipy.constants as spc
import math
from scipy.integrate import odeint
import numpy as np
import rocketODE2stepdeltav as rocket
from scipy import integrate

Me = 5.97219e24 								# Earth mass [kg]
Re = 6371000									# Earth radius [m]

def nav(pos, vel, tAlt):
	t_start = 0
	t_final = 1000
	delta_t = 2
	t = np.linspace(0,100.,1000)
	numsteps = np.floor((t_final-t_start)/delta_t)+1
	initial_conds = [pos[0], vel[0,], pos[1], vel[1], pos[2], vel[2]]
	"""
	r = integrate.ode(orbitFunc).set_integrator('vode', method='bdf')
	r.set_initial_value(initial_conds, t_start)
	"""
	
	
	i = 1
	soln = odeint(orbitFunc, initial_conds, t)
	alt = np.zeros((len(soln),1))
	rx = soln[:,0]
  	ry = soln[:,2]
  	rz = soln[:,4]
  	for i in range(len(soln)-1):
  		alt[i] = np.linalg.norm([rx[i],ry[i], rz[i]])-Re
  	"""
	while r.successful() and i < numsteps:
		
		r.integrate(r.t + delta_t)
		alt[i] = np.linalg.norm([r.y[0], r.y[2], r.y[4]])-Re
		print alt[i]
		if alt[i] <= 0:
			print 'bryt'
			break
		
		rx[i] 	= r.y[0]
		ry[i]	=r.y[2]
		rz[i] = r.y[4]
		i+=1
	"""
	"""
	plt.scatter(rx,ry)
	plt.show()
	"""
	#print np.linalg.norm(pos)-Re,np.amax(alt)
	if np.amax(alt) >= tAlt:
		return True
	else:
		return False

def orbitFunc(w,t):
	positions = np.array([w[0], w[2], w[4]])
	velocities = np.array([w[1], w[3], w[5]])

	grav = rocket.gravAcc(positions)

	accelerations = -grav
	if np.linalg.norm(positions)-Re <= 0:
		return [0,0,0,0,0,0]
	else:
		return [velocities[0], accelerations[0],
			velocities[1], accelerations[1],
			velocities[2], accelerations[2]]

def findHorizVect(pos, vel):
	a = np.cross(pos, np.cross(vel, pos))
	return a/np.linalg.norm(a)
