import RocketSim
import RocketClass
import time as timer
import matplotlib.pyplot as plt
import numpy as np

startTime = timer.time()

R = RocketClass.Rocket(402000., 16000., 3900., 320., 280., 5885.e3, 90720., 3200., 182., 345., 800000., 13000, 0, 10000, 2.5,100)
optional = {'draglosses':False,
			'gravlosses':False,
			'thrust':False,
			'drag':False,
			'pitchangle':False}
data = RocketSim.RocketSimulator(R, 0,0,200000, 1000,1, optional)
print data
plt.scatter(data[0][0], data[0][2])
plt.ylim([-9000000,9000000])
plt.xlim([-9000000,9000000])
plt.show()

print timer.time()-startTime