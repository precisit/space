import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle

tck1 = pickle.load(open('tck1.pk1','rb'))
tck2 = pickle.load(open('tck2.pk1','rb'))

def pressure(alt):
	if (alt<84852):
		P = interpolate.splev(alt,tck1)
	elif (alt<900000):
		P = interpolate.splev(alt,tck2)
	else:
		P=0
	return P
