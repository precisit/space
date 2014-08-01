import numpy as np
from scipy import integrate
import atmofunc
import matplotlib.pyplot as plt
import scipy.constants as consts
import RocketClass
import OrbitCalculations as OC
import time as timer
import ascTime

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
	if "optional" not in param:
		"""
		If no optional returns suggested, check what rocket to be used - predefined or custom?
		Assumes altitude, latitude and longitude are given
		"""
		if 'falcon9' in param:



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

