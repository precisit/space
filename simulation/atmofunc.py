import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle

Ptck1 = pickle.load(open('Pressuretck1.pk1','rb'))
Ptck2 = pickle.load(open('Pressuretck2.pk1','rb'))

Denstck1 = pickle.load(open('Denstck1.pk1','rb'))
Denstck2 = pickle.load(open('Denstck2.pk1','rb'))
dragCoefftck = pickle.load(open('dragCoefftck.pk1','rb'))

def pressure(alt):
	if (alt<84852):
		P = interpolate.splev(alt,Ptck1)
	elif (alt<900000):
		P = interpolate.splev(alt,Pck2)
	else:
		P=0
	return P
def density(alt):
	if (alt<84852):
		P = interpolate.splev(alt,Denstck1)
	elif (alt<900000):
		P = interpolate.splev(alt,Denstck2)
	else:
		P=0
	return P
def dragCoefficient(v):
	#speedofsound mach number etc
