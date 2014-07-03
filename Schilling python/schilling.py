import math
import ascTime
class DeltaVtot:
	
	G = 6.6743e-11
	g = 9.81
	M = 5.97219e24
	rj = 6371000

	def __init__(self, Tmix, alt = 200000, lat = 28):
		self.alt = alt
		self.lat = lat
		self.Tmix = Tmix
		
	def Vcirc(self):
		return Vcirc(self.alt)

	def Vrot(self):
		omega = 2*math.pi/(24*60*60)
		Vrot = omega*DeltaVtot.rj*math.cos(self.lat*math.pi/180)
		return Vrot

	def Vpen(self):
		Hp = self.alt/1000
		K3 = 429.9 + 1.602*Hp + 1.2243e-3*Hp**2
		K4 = 2.328 - 9.687e-4*Hp
		Vpen = K3 + K4*self.Tmix
		return Vpen

	def deltaVtot(self):
		return self.Vcirc() + self.Vpen() - self.Vrot() 
	
def Vcirc(alt):
	Vcirc = math.sqrt(DeltaVtot.M*DeltaVtot.G/(alt+DeltaVtot.rj))
	return Vcirc


#rocket data
Isp1SL = 282
Isp1V = 345
m1wet = 402000
m1dry = 16000
m1res = 30568
T1 = 5886e3 
m1b = m1wet - m1dry - m1res

Isp2V = 345
m2wet = 90720
m2dry = 3200
m2res = 182
T2 = 8e5
m2b = m2wet - m2dry - m2res

A0 = T1/(m1wet + m2wet) # + payload!!!!

#launch data
alt = 200000
lat = 28
Tmix = ascTime.Tmix(m1b, Isp1SL, T1, m2b, Isp2V, T2, Vcirc(alt), Isp1V, A0) # antar haer att deltaVp i schilling = Vcirc


deltaV = DeltaVtot(Tmix, alt, lat)
print "Vcirc: %f" % deltaV.Vcirc()
print "Vrot: %f" % deltaV.Vrot()
print "Tmix: %f" % Tmix
print "Vpen: %f" % deltaV.Vpen()
print "deltaVtot: %f" % deltaV.deltaVtot()
#mp = brentq(deltaV.f, 10000,20000)
#print "mp: %f" % mp