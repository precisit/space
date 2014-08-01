import numpy as np
from scipy import integrate
import atmofunc
import matplotlib.pyplot as plt
import scipy.constants as consts
import RocketClass as RC
import OrbitCalculations as OC
import time as timer
import ascTime
import RocketSim

def pressure(param):
	if "alt" in param:
		return atmofunc.pressure(param["alt"]).tolist(), param["alt"]
	else:
		if not "res" in param:
			param["res"] = 10
		result = np.zeros(param["res"])
		altitudes = np.linspace(param["alt0"],param["alt1"],param["res"])
		for i in range(param["res"]):
			result[i] = atmofunc.pressure(altitudes[i])
		return result.tolist(), altitudes.tolist()

def density(param):
	if "alt" in param:
		return atmofunc.density(param["alt"]).tolist(), param["alt"]
	else:
		if not "res" in param:
			param["res"] = 10
		result = np.zeros(param["res"])
		altitudes = np.linspace(param["alt0"],param["alt1"],param["res"])
		for i in range(param["res"]):
			result[i] = atmofunc.density(altitudes[i])
		return result.tolist(), altitudes.tolist()

def temp(param):
	if "alt" in param:
		return atmofunc.temp(param["alt"]).tolist(), param["alt"]
	else:
		if not "res" in param:
			param["res"] = 10
		result = np.zeros(param["res"])
		altitudes = np.linspace(param["alt0"],param["alt1"],param["res"])
		for i in range(param["res"]):
			result[i] = atmofunc.temp(altitudes[i])
		return result.tolist(), altitudes.tolist()

def RocketSimulator(param):
	rocketparams = {}

	if 'rocket' in param:
		if param['rocket'].lower() == 'ariane5':
			rocketparams['type'] = 'ariane5'
			rocketparams['stats'] = 0
		elif param['rocket'].lower() == 'falcon9':
			rocketparams['type'] = 'falcon9'
			rocketparams['stats'] = 0
		else:
			rocketparams['type'] = 'custom'
			rocketparams['stats'] = params['stats']
	else:
		rocketparams['type'] = 'falcon9'
		rocketparams['stats'] = 0

	if 'payload' in param:
		rocketparams['payload'] = param['payload']
	else:
		"""mpsolver"""
		rocketparams['payload'] = 10000
	if 'pitchAlt' in param:
		rocketparams['gAlt'] = param['pitchalt']
	else:
	 	rocketparams['gAlt'] = 10000

	if 'gmax' in param:
		rocketparams['gmax'] = param['gmax']
	else:
		rocketparams['gmax'] = 1000

	"""Time parameters"""

	if 'tmax' in param:
		tmax = param['tmax']
	else:
		tmax = 5000

	if 'dt' in param:
		dt = param['dt']
	else:
		dt = 1
	if 'longi' in param:
		longi = param['longi']
	else:
		longi = 0

	"""Optional params"""
	if 'optional' not in param:
		optional = {'draglosses':False, 'gravlosses':False, 'thrust':False, 'drag':False, 'pitchangle':False}

	rocket = RC.CreateRocket(rocketparams)
	data = RocketSim.RocketSimulator(rocket, longi, param['lat'], param['alt'], tmax, dt, optional)
	return data


if __name__ == '__main__':
	params1 = {"alt":1}
	params2 = {"alt0":1, "alt1":10000}
	params3 = {"alt0":1, "alt1":10000, "res":30}
	print pressure(params1)
	print pressure(params2)
	print pressure(params3)
	
	print ""
	print ""
	

	print density(params1)
	print density(params2)
	print density(params3)

	print ""
	print ""
	
	print temp(params1)
	print temp(params2)
	print temp(params3)

	asdf = {}
	asdf["pressure"], asdf["alt"] = pressure(params1)
	print asdf

	data = RocketSimulator({'alt':300000, 'lat':0})