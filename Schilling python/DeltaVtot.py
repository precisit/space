import math
from scipy.optimize import brentq
class DeltaVtot:
	
	G = 6.6743e-11
	g = 9.81
	M = 5.97219e24
	rj = 6371000

	def __init__(self, rocket, alt = 200000, lat = 28):
		self.alt = alt
		self.lat = lat
		self.rocket = rocket
		self.rocket["mb1"] = rocket["m1wet"]-rocket["m1res"]-rocket["m1dry"]
		self.rocket["mb2"] = rocket["m2wet"]-rocket["m2res"]-rocket["m2dry"]

		
	def Vcirc(self):
		Vcirc = math.sqrt(DeltaVtot.M*DeltaVtot.G/(self.alt+DeltaVtot.rj))
		return Vcirc
	def Vrot(self):
		omega = 2*math.pi/(24*60*60)
		Vrot = omega*DeltaVtot.rj*math.cos(self.lat*math.pi/180)
		return Vrot
	def Ta(self):
		t1 = self.rocket["mb1"]*self.rocket["Isp1SL"]*DeltaVtot.g/self.rocket["T1"]
		t2 = self.rocket["mb2"]*self.rocket["Isp2V"]*DeltaVtot.g/self.rocket["T2"]
		return t1 + t2
	def Vpen(self):
		Hp = self.alt/1000
		K1 = 662.1 + 1.602*Hp + 1.2243e-3*Hp**2
		K2 = 1.7871 - 9.687e-4*self.alt/1000
		Vpen = K1 + K2*self.Ta()
		return Vpen
	def deltaVtot(self):
		return self.Vcirc() + self.Vpen() - self.Vrot() 
	def f(self,mp):
		Isp1SL = self.rocket["Isp1SL"]
		Isp2V = self.rocket["Isp2V"]
		m01 = self.rocket["m2wet"] + self.rocket["m1wet"] + mp
		m11 = self.rocket["m2wet"] + self.rocket["m1dry"] + mp +self.rocket["m1res"]
		m02 = self.rocket["m2wet"] +mp
		m12 = self.rocket["m2dry"] + self.rocket["m2res"] + mp
		deltav = DeltaVtot.g*(Isp1SL*math.log(m01/m11) + Isp2V*math.log(m02/m12)) -self.deltaVtot()
		return deltav






rocket = {"Isp1SL" : 282, "m1wet" : 402000, "m1dry" : 16000, "m1res" : 30568, "T1" : 5886e3, 
"Isp2V" : 345, "m2wet" : 90720, "m2dry" : 3200, "m2res" : 182, "T2" : 8e5}
deltaV = DeltaVtot(rocket)
print "Vcirc: %f" % deltaV.Vcirc()
print "Vrot: %f" % deltaV.Vrot()
print "Ta: %f" % deltaV.Ta()
print "Vpen: %f" % deltaV.Vpen()
print "deltaVtot: %f" % deltaV.deltaVtot()
mp = brentq(deltaV.f, 10000,20000)
print "mp: %f" % mp