import numpy as np
import scipy.constants as consts
import atmofunc


# Earth constants
Me = 5.97219e24
Re = 6371000
We = np.array([0,0,2*np.pi/(24*60*60)])

def ApsisCalculation(pos,vel):
	"""
	Calculates and returns periapsis anmd apoapsis with the current position and velocity vectors
	"""
	normR1 = np.linalg.norm(pos)
	normV1 = np.linalg.norm(vel)
	gamma1 = AngleBetweenVectors(pos,vel)

	C = 2*consts.G*Me/(normR1*normV1**2)
	D = np.sqrt(C**2-4*(1-C)*(-np.sin(gamma1)**2))

	Rp = normR1*(-C-D)/(2*(1-C))
	Ra = normR1*(-C+D)/(2*(1-C))

	apsides = np.array([np.linalg.norm(normR1*(-C-D)/(2*(1-C))), np.linalg.norm(normR1*(-C+D)/(2*(1-C)))])
	oD = OrthogonalDistance(Ra,Rp)

	return np.array([np.min(apsides), np.max(apsides), oD])

def AngleBetweenVectors(vect1,vect2):
	""" Calculates the angle bewteen two vectors """
	cosang = np.dot(vect1,vect2)
	sinang = np.linalg.norm(np.cross(vect1,vect2))
	return np.arctan2(sinang,cosang)

def OrthogonalDistance(Ra,Rp):
	return 2*Rp*Ra/(Rp + Ra)

def GetOrbitSpeed(radius):
	""" Calculates the orbital speed at altitude radius"""
	return np.sqrt(consts.G*Me/np.linalg.norm(radius))

def GetHorizontalUnitVector(position, velocity):
	""" Returns a unit vector which lies in current horizontal plane for the orbiting body."""
	return np.cross(position, np.cross(velocity, position))

def GetTrueAnomaly(pos, vel):
	""" Calculates the true anomaly, i.e. the angular distance from the periapsis to the orbiting
	body. """
	horizonVector = GetHorizontalUnitVector(pos, vel)
	flighPathAngle = AngleBetweenVectors(horizonVector, vel)
	C = np.linalg.norm(pos)*np.linalg.norm(vel)**2/(consts.G*Me)
	return np.arctan( (C*np.cos(flighPathAngle)*np.sin(flighPathAngle))/(C*np.cos(flighPathAngle)-1) )

def DeltaVToCircular(OrbitRadius, pos, vel):	
	""" Calculates the additional delta-V needed for circular orbit at OrbitRadius
	for the vehicle with position and velocity pos, vel."""

	horizontalUnitVector = lg.GetHorizontalUnitVector(pos, vel)
	desiredVelocity =  GetOrbitSpeed(OrbitRadius)
	currentVelocity = vel*horizontalVector
	return desiredVelocity-currentVelocity

def GetEccentricity(pos, vel):
	""" Calculates the eccentricity of the current orbit """

	apsides = ApsisCalculation(pos,vel)
	periapsis = np.linalg.norm(np.min(apsides))
	apoapsis = np.linalg.norm(np.max(apsides))
	return (apoapsis-periapsis)/(apoapsis+periapsis)

def GetVelocityInOrbit(pos, vel, targetAltitude):
	apsides = ApsisCalculation(pos, vel)
	semiMajorAxis = (np.linalg.norm(apsides[0])+np.linalg.norm(apsides[1]))/2
	print 2./(targetAltitude+Re), 1./semiMajorAxis
	return np.sqrt(consts.G*Me*(2./(targetAltitude)-1./semiMajorAxis))

def TimeToApoapsis(pos, vel):
	""" Calculates the time it will take to reach apoapsis for the vehicle """
	apsides = ApsisCalculation(pos, vel)

	semiMajorAxis = (np.linalg.norm(apsides[0])+np.linalg.norm(apsides[1]))/2

	meanMotion = np.sqrt((consts.G*Me)/semiMajorAxis**3)

	eccentricity = GetEccentricity(pos, vel)

	trueAnomaly = GetTrueAnomaly(pos, vel)

	eccentricAnomalyNow = np.arccos((eccentricity+np.cos(trueAnomaly))/(1+eccentricity*np.cos(trueAnomaly)))
	eccentricAnomalyAtPeriapsis = np.arccos((eccentricity+np.cos(np.pi))/(1+eccentricity*np.cos(np.pi)))

	meanAnomalyNow = eccentricAnomalyNow - eccentricity*np.sin(eccentricAnomalyNow)
	meanAnomalyAtPeriapsis = eccentricAnomalyAtPeriapsis - eccentricity*np.sin(eccentricAnomalyAtPeriapsis)

	timeToApoapsis = (meanAnomalyAtPeriapsis-meanAnomalyNow)/(meanMotion)

	return timeToApoapsis

def CalculateBurnTime(rocket, deltaV):
	""" Calculates how much the rocket will have to perform a burn to increase the deltaV """

	return (rocket.mcurr/rocket.mdotsave)*(1-np.exp(-deltaV/(rocket.isp*consts.g)))

def FlightPathAngle(rocket, altitude):
	""" Calculates and return the recommended flight path angle according
	to MechJeb """
	turnShapeExponent = 0.27
	turnEndAngle = 0

	if altitude < rocket.nAlt: return 90
	if altitude > rocket.targetAltitude: return 0
	return Clamp(90.-((float)(altitude-rocket.nAlt)/(rocket.targetAltitude+5000-rocket.nAlt))**turnShapeExponent*(90.-turnEndAngle),0.0, 89.99)
	
def DownRangeDist(pos1,pos2,t):
	posSurf1 = atmofunc.inertToSurfPos(pos1,t)
	posSurf2 = atmofunc.inertToSurfPos(pos2,t)
	theta = AngleBetweenVectors(posSurf1,posSurf2)
	distance = theta*Re
	return distance 

def Clamp(value, minimum, maximum):
	return np.max(np.array([minimum, np.min( np.array([maximum, value]))]))