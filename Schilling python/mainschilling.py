import math
import schilling
import ascTime
import json
# Script that converts JSON objects to parameters, and inputs them in their designated
# functions. Returns JSON objects containing results



# requires a time for ascention ("Tmix"), an altitude("alt"), 
# a latitude for launch ("lat"), and an inclination ("incl")
def deltaV(params):
	
	
	dVobj = schilling.DeltaVtot(orbPar["Tmix"], orbPar["alt"], orbPar["lat"], orbPar["incl"])
	dVtot = dVobj.deltaVtot()
	dVtotJson = json.dumps({"dVtot":dVtot})
	return dVtotJson

# Requires lots of parameters of the rocket. 
def Tmix(params):
	rockPar = json.loads(params) 
	Tmix = ascTime.Tmix(rockPar["m1b"], rockPar["Isp1SL"], rockPar["T1"], rockPar["m2b"], rockPar["Isp2V"], 
						rockPar["T2"], rockPar["deltaVp"], rockPar["Isp1V"], rockPar["A0"], rockPar["ssT"])
	TmixJson = json.dumps({"Tmix":Tmix})
	return TmixJson


if __name__ == "__main__":
	orbPar = {"Tmix":500,"alt":200000,"lat":28,"incl":28}
	rockPar = {"m1b":40000, "Isp1SL":300, "T1": 70000, "m2b":40000, "Isp2V": 350, "T2":30000, "deltaVp":7788, "Isp1V":290, "A0":13, "ssT": 0}
	params = json.dumps(orbPar)
	paramRock = json.dumps(rockPar)
	print deltaV(params)
	print Tmix(paramRock)

"""
	alt = float(params["alt"][0])
	lat = float(params["lat"][0])
	incl = float(params["incl"][0])

	Isp1SL = float(params["Isp1s"][0])
	Isp1V = float(params["Isp1v"][0])
	T1 = float(params["t1"][0])
	
	Isp2V = float(params["Isp2v"][0])
	T2 = float(params["t2"][0])
	mw1 = float(params["mw1"][0])
	md1 = float(params["md1"][0])
	mr1 = float(params["mr1"][0])

	mw2 = float(params["mw2"][0])
	md2 = float(params["md2"][0])
	mr2 = float(params["mr2"][0])

	m1b = mw1-md1-mr1
	m2b = mw2-md2-mr2 

	mp = float(params["mp"][0])	
	
	A0 = T1/(mw1 + mw2 + mp) # + payload!!!!
	ssT = 0
	deltaVp = schilling.Vcirc(alt) + 1500


	Tmix = ascTime.Tmix(m1b, Isp1SL, T1, m2b, Isp2V, T2, deltaVp, Isp1V, A0, ssT)
	"""