import math
G = 6.6743e-11
g = 9.81
M = 5.97219e24
rj = 6371000
my = G*M
"""
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
"""

# Static functions used for maneuvering
def circToEll(alt1, alt2):
	r1 = alt1 + rj
	r2 = alt2 + rj
	deltaV = math.sqrt(my/r1)*(math.sqrt(2.0*r2/(r1+r2))-1)
	return deltaV

def ellToCirc(alt1, alt2):
	r1 = alt1 + rj
	r2 = alt2 + rj
	deltaV = math.sqrt(my/r2)*(1-math.sqrt(2.0*r1/(r1+r2)))
	return deltaV

#alt1 - altitude in initial orbit
#alt2 - altitude in final
#rb - apoapsis of first ellipsis
def ellToEll(alt1, alt2, rb):
	r1 = alt1 + rj
	r2 = alt2 + rj
	a1 = (alt1+rb)/2+rj
	a2 = (alt2+rb)/2+rj
	deltaV = math.sqrt(2*my/rb-my/a2)-math.sqrt(2*my/rb-my/a1)
	return deltaV

# Performs a Hohmann transfer using two prograde burns, transfering from circular
# to elliptic and elliptic to circular.
def hohmann(params):
	return {"deltaV1":circToEll(params["alt1"],params["alt2"]), "deltaV2":ellToCirc(params["alt1"],params["alt2"])}

"""
This hasn't been checked for correctness!
"""
# Performs a Bi-elliptic transfer using two prograde burns and one retrograde burn,
# transfering from circular to elliptic, elliptic to elliptic and elliptic to circular.
# This maneuver will only be superior to the Hohmann transfer when ratio of final to initial
# semi-major axis is at least 11.94, i.e. when a2/a1 >= 11.94.
def biElliptic(alt1, alt2, rb):
	a = (alt2+rb)/2+rj
	return {"deltaV1":circToEll(params["alt1"], params["rb"]), "deltaV2":ellToEll(params["alt1"], params["alt2"], params["rb"]), "deltaV3"ellToCirc(params["a2"], params["rf"])

#test
print circToCirc(200000, 300000)