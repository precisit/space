import math
G = 6.6743e-11
g = 9.81
M = 5.97219e24
rj = 6371000
my = G*M

@stat
class hohmann:
	def circToEll(alt1, alt2):
		r1 = alt1 + rj
		r2 = alt2 + rj
		deltaV = math.sqrt(my/r1)*(math.sqrt(2*r2/(r1+r2))-1)
		return deltaV
	def ellToCirc(alt1, alt2):
		r1 = alt1 + rj
		r2 = alt2 + rj
		deltaV = math.sqrt(my/r2)*(math.sqrt(2*r1/(r1+r2))-1)
		return deltaV
	def circToCirc(alt1, alt2):
		deltaV = circToEll(alt1,alt2) + ellToCirc(alt1,alt2)
		return deltaV

#test
print hohmann.circToCirc(200000, 300000)