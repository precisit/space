import math
import numpy as np
import scipy.constants as consts

# Earth constants
Me = 5.97219e24
Re = 6371000
We = np.array([0,0,2*math.pi/(24*60*60)])



def ApsisCalculation(r,v):
	"""
	Calculates and returns periapsis anmd apoapsis with the current position and velocity vectors
	"""
	normR1 = np.linalg.norm(r)
	normV1 = np.linalg.norm(v)
	gamma1 = math.acos(np.dot(r,v)/(normR1*normV1))

	C = 2*consts.G*Me/(normR1*normV1**2)
	D = math.sqrt(C**2-4*(1-C)*(-math.sin(gamma1)**2))

	Rp = normR1*(-C-D)/(2*(1-C))
	Ra = normR1*(-C+D)/(2*(1-C))

	return np.array([Rp, Ra])

