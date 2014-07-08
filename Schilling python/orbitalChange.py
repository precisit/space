import math as m
import json
from scipy import constants as const

"""
This program calculates the delta-v's required to change orbits with height 'alt1' to 'alt2'.
It does this by using a Hohmann transfer assuming instantaneous impulses.
"""
params = {"alt1":200000, "alt2":300000}
Me = 5.97219e24		# Mass of the Eart [kg]
Re = 6371000		# earth radius

def hohmannTransfer(params):
	orbitalParams = params
	# enter elliptical orbit at alt1
	deltaV1 = m.sqrt(Me*const.G/(orbitalParams["alt1"]+Re))*(m.sqrt(2*float(orbitalParams["alt2"]+Re)/(orbitalParams["alt1"]+orbitalParams["alt2"]+2*Re))-1)
	# enter circular orbit at alt 2
	deltaV2	= m.sqrt(Me*const.G/(orbitalParams["alt2"]+Re))*(1-m.sqrt(2*float(orbitalParams["alt1"]+Re)/(orbitalParams["alt1"]+orbitalParams["alt2"]+2*Re)))
	# return deltaV
	return {"deltaV1":deltaV1, "deltaV2":deltaV2}


b=hohmannTransfer(params)
print b