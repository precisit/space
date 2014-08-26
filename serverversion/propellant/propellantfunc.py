#import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate
#import matplotlib.pyplot as plt
import pickle
"""
This script simply loads the coefficients for the functions and returns the values of said functions. The functions are:

OMR : Optimum Mixture Ratio
defined on the interval, for liquid oxygen and kerosene:
Pe = [0.1, 1]
and for liquid oxygen and methane:
Pe = [0.1, 1]

AFT : Adiabatic Flame Temperature
defined on the interval, for liquid oxygen and kerosene:
Pe = [2.2, 2.4]
and for liquid oxygen and methane:
Pe = [2.7, 2.9]


GMW : Gas Molecular Weight
defined on the interval, for liquid oxygen and kerosene:
Pe = [2.2, 2.4]
and for liquid oxygen and methane:
Pe = [2.7, 2.9]

SHR : Specific Heat Ratio
defined on the interval, for liquid oxygen and kerosene:
Pe = [2.2, 2.4]
and for liquid oxygen and methane:
Pe = [2.7, 2.9]
"""
OKRtck = pickle.load(open('/home/hans-erik/space/propellant/OK-R.pk1'))
OKMtck = pickle.load(open('/home/hans-erik/space/propellant/OK-M.pk1'))
OKTtck = pickle.load(open('/home/hans-erik/space/propellant/OK-T.pk1'))
OKKtck = pickle.load(open('/home/hans-erik/space/propellant/OK-K.pk1'))
OMRtck = pickle.load(open('/home/hans-erik/space/propellant/OM-R.pk1'))
OMMtck = pickle.load(open('/home/hans-erik/space/propellant/OM-M.pk1'))
OMTtck = pickle.load(open('/home/hans-erik/space/propellant/OM-T.pk1'))
OMKtck = pickle.load(open('/home/hans-erik/space/propellant/OM-K.pk1'))

OKMtck2lines = pickle.load(open('/home/hans-erik/space/propellant/OK-M2lines.pk1'))

def OMR(params):
	if params["fuel"].lower() == 'loxker':
		return OKRtck(params["Pc"],params["Pe"]).tolist()
	elif params["fuel"].lower() == 'loxmeth':
		return OMRtck(params["Pc"],params["Pe"]).tolist()
	else:
		return "fuel not found"

def AFT(params):
	if params["fuel"].lower() == 'loxker':
		return OKTtck(params["Pc"],params["Pe"]).tolist()
	elif params["fuel"].lower() == 'loxmeth':
		return OMTtck(params["Pc"],params["Pe"]).tolist()
	else:
		return "fuel not found"

def GMW(params):
	if params["fuel"].lower() == 'loxker':
		return OKMtck(params["Pc"],params["Pe"]).tolist()
	elif params["fuel"].lower() == 'loxmeth':
		return OMMtck(params["Pc"],params["Pe"]).tolist()
	else:
		return "fuel not found"

def SHR(params):
	if params["fuel"].lower() == 'loxker':
		return OKKtck(params["Pc"],params["Pe"]).tolist()
	elif params["fuel"].lower() == 'loxmeth':
		return OMKtck(params["Pc"],params["Pe"]).tolist()
	else:
		return "fuel not found"

def combData(params):
	if params["fun"].lower() == "omr":
		result = OMR(params)

	elif params["fun"].lower() == "aft":
		result = AFT(params)

	elif params["fun"].lower() == "gmw":
		result = GMW(params)

	elif params["fun"].lower() == "shr":
		result = SHR(params)

	return result.tolist(), params["Pc"], params["Pe"]

if __name__ == '__main__':

	values = np.zeros([2,4,100,10])
	Pe = np.zeros([2,2,10])
	Pe[:,0,:] = np.linspace(0.1,1,10)
	Pe[0,1,:] = np.linspace(2.2,2.4,10)
	Pe[1,1,:] = np.linspace(2.7,2.9,10)
	x = np.linspace(0,250,100)
	for i in range(100):
		for j in range(10):

			values[0,0,i,j] = OMR({"Pc":x[i],"Pe":Pe[0,0,j],"fuel":"loxker"})
			values[1,0,i,j] = OMR({"Pc":x[i],"Pe":Pe[1,0,j],"fuel":"loxmeth"})
			values[0,1,i,j] = AFT({"Pc":x[i],"Pe":Pe[0,1,j],"fuel":"loxker"})
			values[1,1,i,j] = AFT({"Pc":x[i],"Pe":Pe[1,1,j],"fuel":"loxmeth"})
			values[0,2,i,j] = GMW({"Pc":x[i],"Pe":Pe[0,1,j],"fuel":"loxker"})
			values[1,2,i,j] = GMW({"Pc":x[i],"Pe":Pe[1,1,j],"fuel":"loxmeth"})
			values[0,3,i,j] = SHR({"Pc":x[i],"Pe":Pe[0,1,j],"fuel":"loxker"})
			values[1,3,i,j] = SHR({"Pc":x[i],"Pe":Pe[1,1,j],"fuel":"loxmeth"})

	for i in range(4):
		for j in range(10):
			plt.plot(x,values[0,i,:,j])
		plt.show()
	for i in range(4):
		for j in range(10):
			plt.plot(x,values[1,i,:,j])
		plt.show()


	twolines = np.zeros(100) 
	for i in range(10):
		twolines = OKMtck2lines(x,Pe[0,1,i])
		plt.plot(x,twolines,x,values[0,2,:,i])
	plt.show()

