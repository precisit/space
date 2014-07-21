import numpy as np
from scipy import integrate
from matplotlib.pylab import *
from matplotlib import animation
import matplotlib.pyplot as plt
import scipy.constants as consts
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
import atmofunc
import navigation as navi

"""
This is supposed to be an extension of simpleODE, with more forces and function added
to the rocket, such as thrust, thrust vectoring, mass loss, varying air density etc..

"""

Me = 5.97219e24 								# Earth mass [kg]
Re = 6371000									# Earth radius [m]
We = np.array([0,0,2*math.pi/(24*60*60)])		# Earth rotational velocity vector

# vector for saving data
dragForceData = []
ThrData = []
timeData = []
altData = []
deltaVforce = 0.0
deltaVgravloss = 0.0
deltaVdragloss = 0.0

tAltReach = False
vCircReach = False
cutFuel = False
tAlt = 200000

# flag for current stage
stage = 1

# Rocket parameters
Mwet1 = 402000							# Total rocket mass (wet mass) [kg]
Mfuel1 = Mwet1-16000-3900				# Fuel mass	[kg]
IspVAC1 = 320
IspSL1 = 282							# Specific impulse in vaacum [s]
ThrSL1 = 5885e3							# Thrust at sealevel [N]
mdot1 = ThrSL1/(IspSL1*consts.g)		# Fuel burn rate [kg/s]
Ae1 = atmofunc.Ae(IspVAC1,mdot1,ThrSL1) # Area of exit nozzle

Mwet2 = 90720
Mfuel2 = Mwet2-3200-182
IspVAC2 = 345
ThrVAC2 = 800000
mdot2 = ThrVAC2/(IspVAC2*consts.g)
Ae2 = Ae1

Mp = 10000


def rocketfunc(t,w):
	"""
	Function for modelling a projectile motion with thrust, variable mass and drag.

	When this program gets RESTified, we probably should send the parameters below as 
	input arguments.
	"""
	global stage
	global deltaVforce, deltaVgravloss, deltaVdragloss
	global tAltReach, vCircReach, cutFuel, tAlt
	if (stage == 1):
		Mwet = Mwet1 + Mwet2 + Mp
		Mfuel = Mfuel1
		IspVAC = IspVAC1
		mdot = mdot1
		Ae = Ae1

	else:
		Mwet = Mwet2 + Mp
		Mfuel = Mfuel2
		IspVAC = IspVAC2
		mdot = mdot2
		Ae = Ae2

	#angle = (0.001*t**2+0.0*t+90)*math.pi/180 	# Thrust angle - temporary
	positions = np.array([w[0], w[2], w[4]]) 	# Positions
	velocities = np.array([w[1], w[3], w[5]]) 	# Velocities
	alt = norm(positions)-Re
	Vunit = velocities/norm(velocities) 			# Unit velocity vector

	Mburnt = mdot*t									# burnt fuel fuel mass at time t [kg]
 	Mcurr = Mwet-Mburnt	 							# Current mass
 	# If no fuel left, cut mdot
 	gAlt = 14680
 	
 	if alt >= gAlt and not tAltReach:
 		tAltReach = navi.nav(positions, velocities, tAlt)
 	elif tAltReach:
 		#print t
 		mdot = 0
 	
	if Mburnt >= Mfuel:
		if (stage ==1):
			stage = 2
		else:
			mdot = 0
			Mcurr = Mwet-Mfuel
	
	if alt >= tAlt:
		tangentV = navi.findHorizVect(positions, velocities)
		Vunit = tangentV
		print tangentV
		if norm(velocities) >= orbitalVelocity(tAlt):
			mdot = 0
			#print 'orbit', norm(velocities)
	
	dragF = atmofunc.dragForce(velocities, positions)	# Magnitude of the drag force
	grav = gravAcc(positions) 							# Gravitational acceleration
	Thr = atmofunc.thrustEff(IspVAC,Ae,positions,mdot)
	
	#Thrunit = np.array([math.cos(angle),math.sin(angle),0*Vunit[2]])
	
	if alt <= gAlt:
		Thrunit = positions/norm(positions)
	else:
		Thrunit = Vunit
	accelerations = (1/Mcurr)*(-dragF*Vunit + Thr*Thrunit) - grav

	dragForceData.append(dragF)
	ThrData.append(Thr)
	timeData.append(t)
	altData.append(alt)
	deltaVforce += (Thr/Mcurr)*(timeData[len(timeData)-1]-timeData[len(timeData)-2])
	deltaVgravloss += norm(grav)*(timeData[len(timeData)-1]-timeData[len(timeData)-2])
	deltaVdragloss += (dragF/Mcurr)*(timeData[len(timeData)-1]-timeData[len(timeData)-2])
	return [velocities[0], accelerations[0],
			velocities[1], accelerations[1],
			velocities[2], accelerations[2]]




def gravAcc(pos):
	""" Used to calculate the gravity, varying with position """
	F = pos*consts.G*Me/(norm(pos)**3)
	return F

def orbitalVelocity(altm):
	return math.sqrt(consts.G*Me/(Re+altm))

if __name__=='__main__':

	"""Time parameters"""
	t_start = 0.0
	t_final = 40000;
	delta_t = 1;
	numsteps = np.floor((t_final-t_start)/delta_t)+1

 	"""initial params"""

	#Initial launch params
	latDeg = 0 					# Launch latitude in degrees
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
  	r = integrate.ode(rocketfunc).set_integrator('vode', method='bdf')
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
	"""
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(1,1,1)
	ax2.plot(t, velocity, t, altitude)
	plt.show()
	"""
	""" Plotting 2D"""
	print 'DeltaVforce'
	print deltaVforce
	""" 
	print 'DeltaVdragloss'
	print deltaVdragloss
	print 'deltaVgravloss'
	print deltaVgravloss
	"""
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

	plt.plot(timeData,altData)
	plt.title('alt vs time')
	plt.show()
	plt.plot(timeData,dragForceData)
	plt.title('dragForce vs time')
	plt.show()
	plt.plot(timeData,ThrData)
	plt.title('Thr vs time')
	plt.show()
	plt.plot(altData,ThrData)
	plt.title('thrust vs alt')
	plt.show()

	



