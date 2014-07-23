import math
import schilling
import ascTime
from scipy import optimize

"""
Scrip that is used for solving Schillings method combined with the rocket equation
for payload mass.
"""
class mpClass:

	# Constructor that sets the "constant" values for the launch, such as the rockets different masses, thrust,
	# the inclination, latitude and altitude of the orbit.
	def __init__(self, mw1, md1, mr1, Isp1SL, Isp1V, T1, 
				mw2, md2, mr2, Isp2V, T2, alt, lat, incl, ssT):
		self.mw1 = mw1
		self.md1 = md1
		self.mr1 = mr1
		self.Isp1SL = Isp1SL
		self.Isp1V = Isp1V
		self.T1 = T1

		self.mw2 = mw2
		self.md2 = md2
		self.mr2 = mr2
		self.Isp2V = Isp2V
		self.T2 = T2

		self.alt = alt
		self.lat = lat
		self.incl = incl
		self. ssT = ssT

		self.mb1 = mw1-md1-mr1
		self.mb2 = mw2-md2-mr2
	
	# a function of payload mass that is calculated by the difference between the schilling method delta-v, and the 
	# delta-v of the rocket. Since Schillings method requires a deltav to parking orbit, this is approximated using 
	# Townsends method.
	def mpFunc(self, mp):
		A0 = self.T1/(self.mw1 + self.mw2 + mp)
		Ta = ascTime.Ta(self.mb1, self.Isp1SL, self.T1, self.mb2, self.Isp2V, self.T2, self.ssT)
		dVobjTa = schilling.DeltaVtot(Ta, self.alt, self.lat, self.incl)
		deltaVp = dVobjTa.deltaVtot()
		Tmix = ascTime.Tmix(self.mb1, self.Isp1SL, self.T1, self.mb2, self.Isp2V, self.T2, deltaVp, self.Isp1V, A0, self.ssT)
		dVobjTmix = schilling.DeltaVtot(Tmix, self.alt, self.lat, self.incl)
		dVSch = dVobjTmix.deltaVtot()
		m01 = self.mw1 + self.mw2 + mp
		m11 = self.md1 + self.mr1 + self.mw2 + mp
		m02 = self.mw2 + mp
		m12 = self.md2 + self.mr2 + mp
		Isp1avg = (self.Isp1V + self.Isp1SL)/2 								#self.Isp1SL ger en mycket mindre mp
		dVRockeq = ascTime.rockEq(m01, m11, m02, m12, Isp1avg, self.Isp2V)
		return dVSch - dVRockeq

# The solving function which takes the orbit- and rocket parameters and returns the maximum payload. This is solved 
# by using the brentq-method from the scipy-library. The solution for maximum payload mass is assumed to be in the 
# interval [0, mwtot], where mwtot is the total wet mass of the stage-1 and stage-2 rockets
def mpSolve(mw1, md1, mr1, Isp1SL, Isp1V, T1, 
			mw2, md2, mr2, Isp2V, T2, alt, lat, incl, ssT):
	mpObj = mpClass(mw1, md1, mr1, Isp1SL, Isp1V, T1, 
				mw2, md2, mr2, Isp2V, T2, alt, lat, incl, ssT)
	mpMin = 0
	mpMax = mw2 +mw1
	mp = optimize.brentq(mpObj.mpFunc,mpMin,mpMax)
	return mp

#TEST
if __name__ == "__main__":

	Isp1SL = 321
	Isp1V = 363
	m1wet = 2449399
	m1dry = 85729
	m1res = 153638
	T1 = 40061537.0

	Isp2V = 377
	m2wet = 816466
	m2dry = 53070
	m2res = 1527
	T2 = 10430178

	alt = 200000
	lat = 26
	incl = 26
	ssT = 0 			

	print mpSolve(m1wet, m1dry, m1res, Isp1SL, Isp1V, T1, 
			m2wet, m2dry, m2res, Isp2V, T2, alt, lat, incl, ssT)
#	Tmix = ascTime.Tmix(m1b, Isp1SL, T1, m2b, Isp2V, T2, Vcirc(alt), Isp1V, A0, ssT) # antar haer att deltaVp i schilling = Vcirc


#	deltaV = DeltaVtot(Tmix, alt, lat, incl)
"""	
	print ""
	print "data:"
	print ""
	print "Vcirc: %f" % deltaV.Vcirc()
	print "Vrot: %f" % deltaV.Vrot()
	print "Tmix: %f" % Tmix
	print "Vpen: %f" % deltaV.Vpen()
	print "deltaVtot: %f" % deltaV.deltaVtot()
	#mp = brentq(deltaV.f, 10000,20000)
	#print "mp: %f" % mp 

"""
