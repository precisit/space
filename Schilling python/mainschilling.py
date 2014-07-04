import math
import schilling
import ascTime
def deltaV(params):
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
	dVobj = schilling.DeltaVtot(Tmix, alt, lat, incl)
	dVtot = dVobj.deltaVtot()
	
	return dVtot
