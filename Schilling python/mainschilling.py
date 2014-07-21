import math
import schilling
import ascTime
import json
import mpsolver
"""
 Script that holds the main functions, takes parameters, and inputs them in their underlying
 functions. returns dictionaries containing results and approximations made.

"""


	# requires an altitude("alt"), a latitude for launch ("lat"), 
	# and an inclination ("incl"). If no time for ascent is given it it computes it by using Tmix
def deltaV(orbPar):
	approximations = {}
	if ("incl" not in orbPar):
		orbPar["incl"] = orbPar["lat"]
		approximations["inclination"] = orbPar["incl"]
		
	if ("Tmix" in orbPar):
		dVobj = schilling.DeltaVtot(orbPar["Tmix"], orbPar["alt"], orbPar["lat"], orbPar["incl"])
		dVtot = dVobj.deltaVtot()
	else:
		T, approximations = Tmix(orbPar)
		dVobj = schilling.DeltaVtot(T, orbPar["alt"], orbPar["lat"], orbPar["incl"])
		dVtot = dVobj.deltaVtot()
	
	return dVtot, approximations

	# Requires lots of parameters for the rocket. Also does the calculations for the mass of the fuel and approximates
	# a value for deltaVp, if not given. Returns an ascent time "Tmix". 
	# requires minimally 
def Tmix(rockPar):
	gotMb = True
	approximations = {}
	if ("mb1" not in rockPar and "mb2" not in rockPar):
		if("mw1" not in rockPar or "md1" not in rockPar or "mr1" not in rockPar):
			gotMb = False
			print "noMb"
		else:
			rockPar["mb1"] = rockPar["mw1"]-rockPar["md1"]-rockPar["mr1"]
			rockPar["mb2"] = rockPar["mw2"]-rockPar["md2"]-rockPar["mr2"]
			print "mb calculated by mw osv....", rockPar["mb1"],rockPar["mb2"]
	
	if ("mw1" not in rockPar or "mw2" not in rockPar or "mp" not in rockPar):
		rockPar["A0"] = 11.8
		approximations["Acceleration at sealevel"] = rockPar["A0"]
		print "A0=11"
	else:
		rockPar["A0"] = rockPar["T1"]/(rockPar["mw1"] + rockPar["mw2"] + rockPar["mp"])
		print "A0 calculated by T1 mw1 osv", rockPar["A0"]
	
	if ("deltaVp" not in rockPar):
		if ("alt" not in rockPar): 
			rockPar["deltaVp"] = 9300
			print "deltaVp = 9300"
		else:
			rockPar["deltaVp"] = schilling.Vcirc(rockPar["alt"]) + 1500
			print "deltaVp = Vcirc(alt) + 1500", rockPar["deltaVp"]
		approximations["deltaV to parking orbit"] = rockPar["deltaVp"]
	
	if ("ssT" not in rockPar):
		rockPar["ssT"] = 0
		approximations["stage separation time"] = rockPar["ssT"]
		print "ssT = 0"

	if ("Isp1V" not in rockPar):
		if ("Isp1SL" not in rockPar):
			rockPar["Isp1V"] = 320
			print "Isp1V = 320"
		else:
			rockPar["Isp1V"] = 1.1*rockPar["Isp1SL"]
			print "Isp1V = 1.1*Isp1SL", 
		approximations["Isp for stage 1 in vaacum"] = rockPar["Isp1V"]

	if (gotMb):
		
		Tmix = ascTime.Tmix(rockPar["mb1"], rockPar["Isp1SL"], rockPar["T1"], rockPar["mb2"], rockPar["Isp2V"], 
						rockPar["T2"], rockPar["deltaVp"], rockPar["Isp1V"], rockPar["A0"], rockPar["ssT"])
		approximations["Ascent time Tmix calculated to"] = Tmix
		"Tmix calculated by ascTime.Tmix", Tmix

	else:
		Tmix = ascTime.T3s(rockPar["deltaVp"],rockPar["Isp1V"],rockPar["A0"])
		print "Tmix approximated to T3s", Tmix
		approximations["Ascent time Tmix, approximated to T3s"] = Tmix
	return Tmix, approximations

	# requires lots of parameters for the rocket and the orbit. returns a maximum payload for said rocket and orbit.
def mpSolver(mpsolvePar):
	approximations = {}
	if ("ssT" not in mpsolvePar):
		mpsolvePar["sst"] = 0
		approximations["stage separation time"] = rockPar["ssT"]
	
	mp = mpsolver.mpSolve(mpsolvePar["mw1"], mpsolvePar["md1"], mpsolvePar["mr1"], mpsolvePar["Isp1SL"], 
		mpsolvePar["Isp1V"], mpsolvePar["T1"], mpsolvePar["mw2"], mpsolvePar["md2"], mpsolvePar["mr2"], 
		mpsolvePar["Isp2V"], mpsolvePar["T2"], mpsolvePar["alt"], mpsolvePar["lat"], mpsolvePar["incl"], mpsolvePar["ssT"])
	return mp, approximations


if __name__ == "__main__":

	orbPar = {"Tmix":553.83,"alt":200000,"lat":28,"incl":28}
	rockPar = {"mw1":402000,"md1":16000, "mr1":3900, "Isp1SL":282, "Isp1V":320, "T1": 5885e3, "mw2":90720, "md2":3200,"mr2":182, "m2res":182, 
					"Isp2V": 345, "T2":800e3, "alt":200000, "lat": 28, "incl":28, "ssT": 0, "mp":17698}
	mpsolvePar = {"mw1":402000,"md1":16000, "mr1":3900, "Isp1SL":282, "Isp1V":320, "T1": 5885e3, "mw2":90720, "md2":3200,"mr2":182, "m2res":182, 
					"Isp2V": 345, "T2":800e3, "alt":200000, "lat": 28, "incl":28, "ssT": 0}
	dVwoTmixpar = mpsolvePar
	dVwoTmixpar["mp"] = 17698

	deltaV1 = deltaV(orbPar)
	print "deltaV1 med Tmix", deltaV1
	print ""

	del orbPar['Tmix']
	deltaV2 = deltaV(orbPar)
	print "deltaV2 utan Tmix, bara alt, lat, incl", deltaV2
	print ""

	deltaV3 = deltaV(rockPar)
	print "deltaV3 med rockpar for Tmix", deltaV3
	print ""

	mp = mpSolver(mpsolvePar)
	print "mp", mp
	print ""

	TmixT = Tmix(rockPar)
	print "Tmix med alla parametrar", TmixT
	print ""

	BFRpar = {"mw1":2449398.798,"md1":85728.9579, "mr1":153638.54, "Isp1SL":321, "Isp1V":363, "T1":40061523.37, "T2":10430178,"mw2":816466.266, "md2":53070.30729,
			"mr2":1527, "Isp2V":377,"mp":128367,"alt":200000,"incl":26,"lat":26}

	deltaVBFR=deltaV(BFRpar)
	print "deltaVBFR",deltaVBFR
	print ""

	TmixBFR = Tmix(BFRpar)
	print "Tmix BFR", TmixBFR
	print ""

	BFRmp = mpSolver(BFRpar)
	print "BFRmp",BFRmp