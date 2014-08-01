import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle


datapointsx = np.array([[10,25,50,75,100,125,150,175,200,225,250],
						[10,25,50,75,100,125,150,175,200,225,250],
						[10,25,50,75,100,125,150,175,200,225,250]])
						
datapointsvar = np.ones(np.shape(datapointsx))
datapointsvar[0,:] = 0.1*datapointsvar[0,:]
datapointsvar[1,:] = 0.5*(0.1+1)*datapointsvar[1,:]
datapointsvar[2,:] = 1*datapointsvar[2,:]

datapoints2y = np.array([[2.14,2.24,2.31,2.34,2.365,2.38,2.415,2.425,2.435,2.443,2.457],
						[2.1,2.2,2.265,2.3,2.325,2.35,2.37,2.38,2.39,2.405,2.42]])

datapointsy = np.zeros([3,11])
datapointsy[1,:] = (datapoints2y[0,:]+datapoints2y[1,:])/2
datapointsy[0,:] = datapoints2y[0,:]
datapointsy[2,:] = datapoints2y[1,:]
print datapointsx
print datapointsvar
print datapointsy

tck = interpolate.bisplrep(datapointsx,datapointsvar,datapointsy,s=10)
x = np.linspace(10,250,100)
y1 = interpolate.bisplev(x,0.1*np.ones(np.shape(x)),tck)
y2 = interpolate.bisplev(x,1*np.ones(np.shape(x)),tck)
y3 = interpolate.bisplev(x,0.4*np.ones(np.shape(x)),tck)

plt.plot(x,y1,label="pe = 0.1")
plt.plot(x,y2,label="pe = 1")
plt.plot(x,y3,label="pe = 0.6")
plt.legend(("pe = 0.1","pe = 0.6","pe = 1"))
plt.title("lox and kerosene mixture ratio.")
plt.show()
plt.plot(datapointsx[0,:],datapointsy[0,:])
plt.plot(datapointsx[1,:],datapointsy[1,:])
plt.plot(datapointsx[2,:],datapointsy[2,:])
plt.show()
"""
y = interpolate.splev(x,y,tck)
plt.plot(x,y)
plt.plot(datapointsx,datapointsy,'r+')
plt.show()
pickle.dump(tck,open('dragCoefftck.pk1','wb'))
"""