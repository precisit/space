import math
import schilling
import ascTime
import json
import mpsolver
"""
 Script that converts JSON objects to parameters, and inputs them in their designated
 functions. Returns JSON objects containing results

"""


	# requires a time for ascent ("Tmix"), an altitude("alt"), 
	# a latitude for launch ("lat"), and an inclination ("incl")
def deltaV(orbPar):
	#orbPar = json.loads(params) #JSON moved out of schilling and into server, good to do JSON conversion first thing and last thing
	dVobj = schilling.DeltaVtot(orbPar["Tmix"], orbPar["alt"], orbPar["lat"], orbPar["incl"])
	dVtot = dVobj.deltaVtot()
	#dVtotJson = json.dumps({"dVtot":dVtot})
	return dVtot

	# Requires lots of parameters for the rocket. Also does the calculations for the mass of the fuel and approximates
	# a value for deltaVp, if not given. Returns an ascent time "Tmix"
def Tmix(params):
	rockPar = json.loads(params)
	
	rockPar["mb1"] = rockPar["mw1"]-rockPar["md1"]-rockPar["mr1"]
	rockPar["mb2"] = rockPar["mw2"]-rockPar["md2"]-rockPar["mr2"]
	rockPar["A0"] = rockPar["T1"]/(rockPar["mw1"] + rockPar["mw2"] + rockPar["mp"])
	if ("deltaVp" not in rockPar):
		rockPar["deltaVp"] = 9300

	Tmix = ascTime.Tmix(rockPar["mb1"], rockPar["Isp1SL"], rockPar["T1"], rockPar["mb2"], rockPar["Isp2V"], 
						rockPar["T2"], rockPar["deltaVp"], rockPar["Isp1V"], rockPar["A0"], rockPar["ssT"])
	TmixJson = json.dumps({"Tmix":Tmix})
	return TmixJson

	# requires lots of parameters for the rocket and the orbit. returns a maximum payload for said rocket and orbit.
def mpSolver(params):
	mpsolvePar = json.loads(params)
	mp = mpsolver.mpSolve(mpsolvePar["mw1"], mpsolvePar["md1"], mpsolvePar["mr1"], mpsolvePar["Isp1SL"], 
		mpsolvePar["Isp1V"], mpsolvePar["T1"], mpsolvePar["mw2"], mpsolvePar["md2"], mpsolvePar["mr2"], 
		mpsolvePar["Isp2V"], mpsolvePar["T2"], mpsolvePar["alt"], mpsolvePar["lat"], mpsolvePar["incl"], mpsolvePar["ssT"])
	mpJson = json.dumps({"mp":mp})
	return mpJson

	#testprogram
if __name__ == "__main__":
	orbPar = {"Tmix":500,"alt":200000,"lat":28,"incl":28}
	rockPar = {"mw1":402000,"md1":16000, "mr1":3900, "Isp1SL":282, "Isp1V":320, "T1": 5885e3, "mw2":90720, "md2":3200,"mr2":182, "m2res":182, 
					"Isp2V": 345, "T2":800e3, "alt":200000, "lat": 28, "incl":28, "ssT": 0, "mp":17362}
	mpsolvePar = {"mw1":402000,"md1":16000, "mr1":3900, "Isp1SL":282, "Isp1V":320, "T1": 5885e3, "mw2":90720, "md2":3200,"mr2":182, "m2res":182, 
					"Isp2V": 345, "T2":800e3, "alt":200000, "lat": 28, "incl":28, "ssT": 0}
	params = json.dumps(orbPar)
	paramRock = json.dumps(rockPar)
	paramMpsolve = json.dumps(mpsolvePar)
	print mpSolver(paramMpsolve)
	print deltaV(params)
	print Tmix(paramRock)
	