import numpy as np
import matplotlib.pyplot as plt
import atmofunc
import RocketSim
Re = RocketSim.Re

def Clamp(value, minimum, maximum):
	return np.max(np.array([minimum, np.min( np.array([maximum, value])) ]))

class AscentPath:
	"""
	turnStartAltitude
	turnEndAltitude
	turnEndAngle
	turnShapeExponent = 0.4
	desiredOrbitAltitude
	"""

	def __init__(self, turnStartAltitude, turnEndAltitude, desiredOrbitAltitude,turnEndAngle=0, turnShapeExponent=0.35):
		self.turnStartAltitude=turnStartAltitude
		self.turnEndAltitude=turnEndAltitude
		self.desiredOrbitAltitude=desiredOrbitAltitude
		self.turnEndAngle=turnEndAngle
		self.turnShapeExponent=turnShapeExponent

	def FlightPathAngle(self, altitude):

		if altitude < self.turnStartAltitude: return 90
		if altitude > self.turnEndAltitude: return self.turnEndAngle
		return Clamp(90.-((float)(altitude-self.turnStartAltitude)/(self.turnEndAltitude-self.turnStartAltitude))**self.turnShapeExponent*(90.-self.turnEndAngle),0.0, 89.99)

"""
class Pilot:
	def __init__(self, turnStartAltitude, turnEndAltitude, desiredOrbitAltitude, turnStartAltitude=0, turnShapeExponent=0.4):
		self.AP = AscentPath(turnStartAltitude, turnEndAltitude, desiredOrbitAltitude, turnStartAltitude, turnShapeExponent)
		self.verticalAscent = True
		self.gravityTurn = False
		self.coastToApoapsis = False
		self.circularize = False

	def Drive(self, AscentPath, pos, vel):

		altitude = np.linalg.norm(pos)-Re


		if altitude < AscentPath.turnStartAltitude:

		elif altitude >= AscentPath.turnStartAltitude and altitude < AscentPath.turnEndAltitude:

		elif altitude

		def VerticalAscent():
			ThrUnit = atmofunc.unit(pos)
		def GravityTurn():
			ThrUnit
		def CoastToApoapsis():

		def Circularize():
"""

if __name__ == '__main__':

	alts = np.array(range(0,230000))

	Apath = AscentPath(10000, 200000, 200000,0,0.3)
	angles = np.zeros((len(alts),1))
	for i in range(len(alts)):
		angles[i] = Apath.FlightPathAngle(alts[i])

	plt.plot(ranges,alt)
	plt.show()