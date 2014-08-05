import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle

asdftck = pickle.load(open('OK-R.pk1'))
x=np.linspace(0,250,100)
plt.plot(x,asdftck(x,0.1))
plt.show()