import numpy as np
import matplotlib.pyplot as plt

posx = np.linspace(0,100,100)
posy = np.linspace(0,100,100)
#plt.scatter(posx,posy)
#plt.show()
vel = 10*np.ones(100)
plt.quiver(posx,posy,vel,vel)
plt.show()