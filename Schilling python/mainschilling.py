import math
import schilling
import ascTime
import json
import mpsolver
"""
 Script that holds the main functions, takes parameters, and inputs them in their underlying
 functions. returns dictionaries containing results

"""


	# requires a time for ascent ("Tmix"), an altitude("alt"), 
	# a latitude for launch ("lat"), and an inclination ("incl")
def deltaV(orbPar):
	if ("Tmix" in orbPar):
		dVobj = schilling.DeltaVtot(orbPar["Tmix"], orbPar["alt"], orbPar["lat"], orbPar["incl"])
		dVtot = dVobj.deltaVtot()
	elif(("mw1" in orbPar and "mw2" in orbPar) or ("mb1" in orbPar and "mb2" in orbPar)):
		dVtot = deltaVwoTmix(orbPar)
	else:
		deltaVp = schilling.Vcirc(orbPar["alt"]) + 1500
		Isp = 320
		A0 = 11
		Time = ascTime.T3s(deltaVp,Isp,A0)
		dVobj = schilling.DeltaVtot(500, orbPar["alt"], orbPar["lat"], orbPar["incl"])
		dVtot = dVobj.deltaVtot()
	return dVtot

	# Requires lots of parameters for the rocket. Also does the calculations for the mass of the fuel and approximates
	# a value for deltaVp, if not given. Returns an ascent time "Tmix"
def Tmix(rockPar):
	rockPar["mb1"] = rockPar["mw1"]-rockPar["md1"]-rockPar["mr1"]
	rockPar["mb2"] = rockPar["mw2"]-rockPar["md2"]-rockPar["mr2"]
	rockPar["A0"] = rockPar["T1"]/(rockPar["mw1"] + rockPar["mw2"] + rockPar["mp"])
	if ("deltaVp" not in rockPar):
		rockPar["deltaVp"] = 9300

	Tmix = ascTime.Tmix(rockPar["mb1"], rockPar["Isp1SL"], rockPar["T1"], rockPar["mb2"], rockPar["Isp2V"], 
						rockPar["T2"], rockPar["deltaVp"], rockPar["Isp1V"], rockPar["A0"], rockPar["ssT"])
	return Tmix

	# requires lots of parameters for the rocket and the orbit. returns a maximum payload for said rocket and orbit.
def mpSolver(mpsolvePar):
	mp = mpsolver.mpSolve(mpsolvePar["mw1"], mpsolvePar["md1"], mpsolvePar["mr1"], mpsolvePar["Isp1SL"], 
		mpsolvePar["Isp1V"], mpsolvePar["T1"], mpsolvePar["mw2"], mpsolvePar["md2"], mpsolvePar["mr2"], 
		mpsolvePar["Isp2V"], mpsolvePar["T2"], mpsolvePar["alt"], mpsolvePar["lat"], mpsolvePar["incl"], mpsolvePar["ssT"])
	return mp

	# Calculates deltav without needing Tmix. Needs other parameters for the rocket though. Makes an estimation of deltaVP needed
	# for schillings Tmix using townsends method. 
def deltaVwoTmix(param):
	if ("mb1" not in param and mb2 not in param):
		param["mb1"] = param["mw1"]-param["md1"]-param["mr1"]
		param["mb2"] = param["mw2"]-param["md2"]-param["mr2"]
	
	param["A0"] = param["T1"]/(param["mw1"] + param["mw2"] + param["mp"])
	Ta = ascTime.Ta(param["mb1"], param["Isp1SL"], param["T1"], param["mb2"], param["Isp2V"], param["T2"], param["ssT"])
	dVobjTa = schilling.DeltaVtot(Ta, param["alt"], param["lat"], param["incl"])
	deltaVp = dVobjTa.deltaVtot()
	Tmix = ascTime.Tmix(param["mb1"], param["Isp1SL"], param["T1"], param["mb2"], param["Isp2V"], 
						param["T2"], deltaVp, param["Isp1V"], param["A0"], param["ssT"])
	dVobjTmix = schilling.DeltaVtot(Tmix, param["alt"], param["lat"], param["incl"])
	dVTmix = dVobjTmix.deltaVtot()
	return dVTmix
	#testprogram

if __name__ == "__main__":

	orbPar = {"Tmix":553.83,"alt":200000,"lat":28,"incl":28}
	rockPar = {"mw1":402000,"md1":16000, "mr1":3900, "Isp1SL":282, "Isp1V":320, "T1": 5885e3, "mw2":90720, "md2":3200,"mr2":182, "m2res":182, 
					"Isp2V": 345, "T2":800e3, "alt":200000, "lat": 28, "incl":28, "ssT": 0, "mp":17698}
	mpsolvePar = {"mw1":402000,"md1":16000, "mr1":3900, "Isp1SL":282, "Isp1V":320, "T1": 5885e3, "mw2":90720, "md2":3200,"mr2":182, "m2res":182, 
					"Isp2V": 345, "T2":800e3, "alt":200000, "lat": 28, "incl":28, "ssT": 0}
	dVwoTmixpar = mpsolvePar
	dVwoTmixpar["mp"] = 17698

	mp = mpSolver(mpsolvePar)
	deltaV1 = deltaV(orbPar)
	deltaV2 = deltaV( dVwoTmixpar )
	del orbPar['Tmix']
	deltaV3 = deltaV(orbPar)
	Tmix = Tmix(rockPar)
	deltaVwoTmix = deltaVwoTmix(dVwoTmixpar)

	print "deltaVwoTmix", deltaVwoTmix
	print "deltaV2", deltaV2
	print "mp", mp
	print "deltaV1", deltaV1
	print "Tmix", Tmix
	print "deltaV3", deltaV3