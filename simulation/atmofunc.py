import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle
import math

Ptck1 = pickle.load(open('Pressuretck1.pk1'))
Ptck2 = pickle.load(open('Pressuretck2.pk1'))

Denstck1 = pickle.load(open('Denstck1.pk1'))
Denstck2 = pickle.load(open('Denstck2.pk1'))

Ttck1 = pickle.load(open('Ttck1.pk1'))
Ttck2 = pickle.load(open('Ttck2.pk1'))

dragCoefftck = pickle.load(open('dragCoefftck.pk1'))

def pressure(alt):
	if (alt<84852):
		P = interpolate.splev(alt,Ptck1)
	elif (alt<900000):
		P = interpolate.splev(alt,Ptck2)
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

#problem med modellen vid ca 80000
def temp(alt):
	if (alt<84852):
		P = interpolate.splev(alt,Ttck1)
	elif (alt<900000 and alt>100000):
		P = interpolate.splev(alt,Ttck2)
	elif (alt<900000):
		P = 0.000000043284*alt**2 - 0.008195*alt + 570.657216
	else:
		P=1011.5379
	return P
def dragCoefficient(v,alt):
	mach = v/(20.0457*math.sqrt(temp(alt)))
	CD = interpolate.splev(mach,dragCoefftck)
	return CD
	
	#  "A is the area of the body normal to the flow". The saturn V has an area of 113 m^2 
def dragForce(v,alt,A=113):
	CD = dragCoefficient(v,alt)
	#print CD
	rho = density(alt)
	#print rho
	FD = 0.5*CD*rho*v**2
	#print FD
	return FD

if __name__=="__main__":
	uppl = 400
	alt = np.linspace(0,200000,uppl)
	v = np.linspace(0,9000,uppl)
	
	P = np.zeros(uppl)
	dens = np.zeros(uppl)
	T = np.zeros(uppl)
	CD = np.zeros(uppl)
	FD = np.zeros(uppl)




	for i in range(np.shape(alt)[0]):
		
		P[i] = pressure(alt[i])
		dens[i] = density(alt[i])
		T[i] = temp(alt[i])
		CD[i] = dragCoefficient(v[i],alt[i])
		FD[i] = dragForce(v[i],alt[i])
		
		

	
	plt.plot(alt,P)
	plt.show()
	plt.plot(alt,dens)
	plt.show()
	plt.plot(alt,T)
	plt.show()
	plt.plot(alt,CD)
	plt.show()
	plt.plot(alt,FD)
	plt.show()