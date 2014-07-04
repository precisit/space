import math
import ascTime
class DeltaVtot:
	
	G = 6.6743e-11
	g = 9.81
	M = 5.97219e24
	rj = 6371000

	def __init__(self, Tmix, alt = 200000, lat = 28, incl = 28):
		self.alt = alt
		self.lat = lat
		self.Tmix = Tmix
		self.incl = incl

	def Vcirc(self):
		return Vcirc(self.alt)

	def Vrot(self):
		omega = 2*math.pi/(24*60*60)
		Vrot = omega*DeltaVtot.rj*math.cos(self.lat*math.pi/180)*math.cos(self.incl*math.pi/180) #cos*cos?
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
Isp1SL = 321
Isp1V = 363
m1wet = 2449399
m1dry = 85729
m1res = 153638
T1 = 40061537.0
m1b = m1wet - m1dry - m1res


Isp2V = 377
m2wet = 816466
m2dry = 53070
m2res = 1527
T2 = 10430178
m2b = m2wet - m2dry - m2res

mp = 128367

A0 = T1/(m1wet + m2wet + mp) # + payload!!!!
print "A0", A0

#launch data
alt = 200000
lat = 26
incl = 26
ssT = 0 						# stage separation time. antar ingen thrust under denna tid
Tmix = ascTime.Tmix(m1b, Isp1SL, T1, m2b, Isp2V, T2, Vcirc(alt), Isp1V, A0, ssT) # antar haer att deltaVp i schilling = Vcirc


deltaV = DeltaVtot(Tmix, alt, lat, incl)
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