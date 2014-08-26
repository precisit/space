import numpy as np
from scipy import interpolate
#import matplotlib.pyplot as plt
import pickle

"""
script for yielding a function of the drag coefficient from graph at http://www.braeunig.us/apollo/saturnV.htm
"""

datapointsx = np.array([0  , 0.5,  1.0, 1.2, 1.4, 1.85, 2.3,  4.9,8.5, 9.0, 10.0])
datapointsy = np.array([0.3, 0.26, 0.4, 0.5, 0.55, 0.5, 0.4, 0.2, 0.258,0.26, 0.26])
print datapointsx
print datapointsy
tck = interpolate.splrep(datapointsx,datapointsy)
x = np.linspace(0,10,101)
y = interpolate.splev(x,tck)
plt.plot(x,y)
plt.plot(datapointsx,datapointsy,'r+')
plt.show()
pickle.dump(tck,open('dragCoefftck.pk1','wb'))