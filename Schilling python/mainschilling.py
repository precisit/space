import math
import schilling
def deltaV(params):
	alt = float(params["alt"][0])
	Vcirc = schilling.Vcirc(alt)
	return Vcirc
	#{"alt": ["12345"],}