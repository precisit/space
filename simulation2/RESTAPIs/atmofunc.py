import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle
import scipy.constants as constants

Re = 6371000
We = np.array([0,0,np.pi*2./(24*3600)])


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
	mach = v/(20.0457*np.sqrt(temp(alt)))
	CD = interpolate.splev(mach,dragCoefftck)
	return CD
	
	#  "A is the area of the body normal to the flow". The saturn V has an area of 113 m^2 
def dragForce(vi,ri, A=113):
	vr, alt = inertToSurf(vi,ri)
	v = np.linalg.norm(vr)
	CD = dragCoefficient(v,alt)
	rho = density(alt)
	FD = 0.5*A*CD*rho*v**2
	return FD



def inertToSurf(vi,ri):
	vr = inertToSurfVel(vi,ri)
	alt = inertToAlt(ri)
	return vr,alt

def inertToAlt(ri):
	alt = np.linalg.norm(ri)-Re
	return alt

def inertToSurfVel(vi,ri):
	vr = vi - np.cross(We,ri)
	return vr

def inertToSurfPos(ri,t):
	omega = np.linalg.norm(We)
	Rot = np.array([[np.cos(-omega*t), -np.sin(-omega*t), 0], 
					[np.sin(-omega*t), np.cos(-omega*t), 0],
					[0, 0, 1]])
	rr = np.dot(ri,Rot)
	return rr

def surfToInertPos(rr,t):
	omega = np.linalg.norm(We)
	Rot = np.array([[np.cos(omega*t), -np.sin(omega*t), 0], 
					[np.sin(omega*t), np.cos(omega*t), 0],
					[0, 0, 1]])
	ri = np.dot(rr,Rot)
	return ri
def unit(vec):
	norm = np.linalg.norm(vec)
	if norm == 0:
		unit = np.array([0,0,0])
	else:
		unit = vec/norm
	return unit

	# efficient thrust as a function of position and current massflow. Ae is the area of the nozzle exit.
def thrustEff(Ispvac,Ae,r,mdot, ispb=0, mdotb=0,Aeb=0,):
	alt = inertToAlt(r)
	Teff = Ispvac*constants.g*mdot+ispb*constants.g*mdotb- (Ae+Aeb)*pressure(alt)
	if (Teff<0):
		Teff=0
	return Teff

def Ae(Ispvac,mdotmax,FSL):
	return (Ispvac*constants.g*mdotmax-FSL)/101325 



if __name__=="__main__":
	uppl = 200
	altitude = 200000
	r = np.zeros([uppl,3])
	v = np.zeros([uppl,3])
	alt = np.linspace(0,altitude,uppl)
	r[:,0] = np.linspace(0,altitude,uppl) + Re
	v[:,0] = np.linspace(0,9000,uppl)
	v[:,1] = 463.3*np.ones(uppl)
	
	

	P = np.zeros(uppl)
	dens = np.zeros(uppl)
	T = np.zeros(uppl)
	#CD = np.zeros(uppl)
	FD = np.zeros(uppl)
	Thrust = np.zeros(uppl)
	Ae = Ae(320,236.047,654000)
	print Ae



	for i in range(np.shape(FD)[0]):
		
		P[i] = pressure(alt[i])
		dens[i] = density(alt[i])
		T[i] = temp(alt[i])
		#CD[i] = dragCoefficient(v[i],alt[i])
		
		FD[i] = dragForce(v[i,:],r[i,:])
		Thrust[i] = thrustEff(320,Ae,r[i,:],236.047)
		
		

	
	plt.plot(alt,P)
	plt.title('pressure')
	plt.show()
	plt.plot(alt,dens)
	plt.title('dens')
	plt.show()
	plt.plot(alt,T)
	plt.title('temp')
	plt.show()
	#plt.plot(alt,CD)
	#plt.title('dragCoefficient')
	#plt.show()
	
	plt.plot(r[:,0],FD)
	
	plt.title('dragForce')
	plt.show()

	plt.plot(r[:,0],Thrust)
	plt.title('Thrust')
	plt.show()

	print pressure(np.array([1,2,3,4,5,6]))