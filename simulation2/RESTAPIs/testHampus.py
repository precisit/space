import RocketSim
import RocketClass3stage
import time as timer
import matplotlib.pyplot as plt
import numpy as np

startTime = timer.time()

R = RocketClass3stage.CreateRocket({'type':'saturnv', 'payload':20000, 'gAlt':20000, 'gmax':100})
optional = {'draglosses':False,
			'gravlosses':False,
			'thrust':False,
			'drag':False,
			'pitchangle':False}
data = RocketSim.RocketSimulator(R, 90,0,200000, 10000,1, optional)
print data
plt.scatter(data[0][0], data[0][1])
plt.ylim([-9000000,9000000])
plt.xlim([-9000000,9000000])
plt.show()

print timer.time()-startTime