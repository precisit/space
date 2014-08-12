import math
import matplotlib.pyplot as plt
import numpy as np

alt = range(10000,100000)
vertAscentEnd = 10000.
turnEnd = 40000.
TurnEndAngle = 0.

a = np.zeros((len(alt),1))

def Clamp(value, minimum, maximum):
	return np.max(np.array([minimum, np.min( np.array([maximum, value])) ]))

for i in range(len(alt)):
	a[i] = (90-((alt[i]-vertAscentEnd)/(turnEnd-vertAscentEnd))**0.3*(90.-turnEnd))#,0.01, 89.99)
maxA = np.max(a[i])

a *= 90/maxA

plt.plot(alt,a)
plt.show()

