import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle

OKRtck = pickle.load(open('OK-R.pk1'))
OKMtck = pickle.load(open('OK-M.pk1'))
OKTtck = pickle.load(open('OK-T.pk1'))
OKKtck = pickle.load(open('OK-K.pk1'))

def OMRloxker(Pc,Pe):
	return OKRtck(Pc,Pe)

def AFTloxker(Pc,Pe):
	return OKTtck(Pc,Pe)

def GMWloxker(Pc,Pe):
	return OKMtck(Pc,Pe)

def SHRloxker(Pc,Pe):
	return OKKtck(Pc,Pe)


if __name__ == '__main__':

	x=np.linspace(0,250,100)
	plt.plot(x,OMRloxker(x,0.1))
	plt.show()

	print OMRloxker(0,0)
	print OMRloxker(100,1)

	plt.plot(x,AFTloxker(x,2.2))
	plt.show()

	print AFTloxker(0,0)
	print AFTloxker(125,2.3)

	x=np.linspace(0,250,100)
	plt.plot(x,GMWloxker(x,2.3))
	plt.show()

	print GMWloxker(0,0)
	print GMWloxker(125,2.4)

	plt.plot(x,SHRloxker(x,2.2))
	plt.show()

	print SHRloxker(0,0)
	print SHRloxker(75,2.2)