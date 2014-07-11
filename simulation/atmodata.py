import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle
"""
this is a script that takes the numerical values of the www.braeunig.us/space/amos.html ,
makes interpolating functions and saves the function parameters for use in atmofunc.py 
"""
Hbra=0

Tbralow = 1
Pbralow = 2

Densbralow = 3
Densbraupp = 6

Tbraupp = 5
Pbraupp = 7

# change what property you want to export a function of
proplow = Densbralow 
propupp = Densbraupp
# change what the name of the data should be
tck1name = 'Denstck1.pk1'
tck2name = 'Denstck2.pk1'

# loading data from http://www.braeunig.us/space/atmos.htm 
# model of the atmosphere. using values for mean solar activity

upperatm = np.loadtxt("braeunig_upper_atm.txt")
loweratm = np.loadtxt("braeunig_lower_atm.txt")
upperatm[:,Hbra]=1000*upperatm[:,Hbra]

# plotting vectors
x1 = np.linspace(-2000,100000,50)
x2 = np.linspace(0,900000,50)


# interpolating both the model of the upper and lower atmosphere. Not using the 
# first 4 rows of data in the upper atmosphere
tck1 = interpolate.splrep(loweratm[:,Hbra],loweratm[:,proplow])
tck2 = interpolate.splrep(upperatm[4:,Hbra],upperatm[4:,propupp])
#plt.xlim(left=-2000, right=900000)
#plt.ylim(bottom=0,top=1)
#plt.plot(upperatm[:,Hbra],upperatm[:,Pbraupp], 'bo')
plt.plot(loweratm[:,Hbra],loweratm[:,proplow], 'r+')
plt.plot(x1,interpolate.splev(x1,tck1))

plt.show()

plt.plot(upperatm[:,Hbra],upperatm[:,propupp], 'r+')
plt.plot(x2,interpolate.splev(x2,tck2))

plt.show()

# function using both the upper and lower atmosphere to return propsure. 
# this function will exist in atmofunc.py aswell
def func(alt):
	if (alt<84852):
		P = interpolate.splev(alt,tck1)
	elif (alt<900000):
		P = interpolate.splev(alt,tck2)
	else:
		P=0
	return P

# testing the func() function
alt = np.linspace(-2000,1200000,1000)
prop = np.zeros(np.shape(alt))
for i in range(np.shape(alt)[0]):
	prop[i]=func(alt[i])

#creating vectors for both upper and lower atmosphere
totatmH = np.zeros(67)
totatmProp = np.zeros(67)
totatmH[0:26] = loweratm[:,Hbra]
totatmH[26:] = upperatm[5:,Hbra]

totatmProp[0:26] = loweratm[:,proplow]
totatmProp[26:] = upperatm[5:,propupp]


plt.plot(totatmH,totatmProp, 'r+')
plt.plot(alt,prop)

plt.show()

# saving the modeled interpolationfunctions for use in atmofunc.py
pickle.dump(tck1,open(tck1name,'wb'))
pickle.dump(tck2,open(tck2name,'wb'))
#tck1loaded = pickle.load(open('tck1.pk1','rb'))

