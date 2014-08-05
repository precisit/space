import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle
from pylab import ginput, axis
from mpl_toolkits.mplot3d import Axes3D

source = str(raw_input("file? (<l> to load last known values):"))

if source is "l":
	datain = np.load("xyvalues.npy")
	Pe = np.load("Pevalues.npy")
	numoflines = np.load("input.npy")[0]
	numClicks = np.load("input.npy")[1]
	left = np.load("input.npy")[2]
	right = np.load("input.npy")[3]
	lower = np.load("input.npy")[4]
	upper = np.load("input.npy")[5]

else:

	currimg = mpimg.imread(source)

	numoflines = int(raw_input("how many lines?:"))
	numClicks = int(raw_input("number of clicks?"))
	datain = np.zeros([numoflines,numClicks,2])
	Pe = np.zeros([numoflines,numClicks])
	for i in range(numoflines):
		plt.imshow(currimg)
		curr = np.array(ginput(numClicks, timeout=100))
		datain[i,:,:] = curr
		Pecurr = float(raw_input("Pe?:"))
		Pe[i,:] = np.ones(numClicks)*Pecurr
		plt.show()

	left = float(raw_input("left:"))
	right = float(raw_input("right:"))
	lower = float(raw_input("lower:"))
	upper = float(raw_input("upper:"))


	datain[:,:,1] = currimg.shape[0] - datain[:,:,1]
	datain[:,:,0] = left + (right-left)*datain[:,:,0]/currimg.shape[1]
	datain[:,:,1] = lower + (upper-lower)*datain[:,:,1]/currimg.shape[0]


	while len(Pe[:,0]) < numClicks:
		length = 2*len(Pe[:,0])-1
		meanArr = np.zeros([len(Pe[:,0])-1, numClicks, 2])
		meanArrPe = np.zeros([len(Pe[:,0])-1, numClicks])
		
		Penew = np.zeros([length, numClicks])
		datainnew = np.zeros([length, numClicks,2])
		
		Penew[0:length:2,:] = Pe
		datainnew[0:length:2,:,:] = datain
		j=0
		while j < len(Pe[:,0]) - 1:
			meanArr[j,:,:] = 0.5*(datain[j,:,:] + datain[j+1,:,:])
			meanArrPe[j,:] = 0.5*(Pe[j,:] + Pe[j+1,:])
			j = j+1

		datainnew[1:length-1:2,:,:] = meanArr
		Penew[1:length-1:2,:] = meanArrPe

		Pe = Penew
		datain = datainnew


	np.save("xyvalues",datain)
	np.save("Pevalues",Pe)
	np.save("input",np.array([numoflines,numClicks,left,right,lower,upper]))

for i in range(len(datain[:,0,0])):
	plt.plot(datain[i,:,0],datain[i,:,1])
	
plt.show()


allx = datain[0,:,0]
allPe = Pe[0,:]

ally = datain[0,:,1]
i=1
while i < len(Pe[:,0]):
	allx = np.append(allx, datain[i,:,0])
	allPe = np.append(allPe, Pe[i,:])
	ally = np.append(ally, datain[i,:,1])
	i = i+1

allpoints = np.array([allx,allPe]).T


tck = interpolate.CloughTocher2DInterpolator(allpoints,ally)
x = np.linspace(allx.min(),allx.max(),200)
Peplot = np.linspace(Pe[0,0], Pe[len(Pe)-1,0], 200)

for i in range(len(Peplot)):
	plt.plot(x,tck(x,Peplot[i]))

for i in range(len(datain[:,0,0])):
	plt.plot(datain[i,:,0],datain[i,:,1],'r+')

plt.show()

savefile = str(raw_input("file for saving function variables? (<n> to cancel save):"))
if savefile is not "n":
	pickle.dump(tck,open(savefile,'wb'))
	print "saved as ",savefile
