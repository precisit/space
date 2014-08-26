import matplotlib.image as mpimg
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pickle
from pylab import ginput, axis
from mpl_toolkits.mplot3d import Axes3D

"""
Script for interpolation in 2 dimensions. The user specifies file to load and dimensions of the 
image. Points to interpolate are defined by the mouse clicks of the user in the image. 

"""
source = str(raw_input("file? (<l> to load last known values):"))
#
# The image file to load must be in the format .png. The command 'l' loads previous values.
#
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
	
	#
	# When the user has clicked the specified number of times, the previous clicks will not be visible
	# and the user must close the current image. The program then asks for the value 'Pe' which is the
	# constant value representing the line on the graph. This will iterate a number of times based on the 
	# number of lines
	#
	
	for i in range(numoflines):
		plt.imshow(currimg)
		curr = np.array(ginput(numClicks, timeout=100))
		datain[i,:,:] = curr
		Pecurr = float(raw_input("Pe?:"))
		Pe[i,:] = np.ones(numClicks)*Pecurr
		plt.show()
	#
	# These values are the dimension of the image from which to extrapolate
	#

	left = float(raw_input("left:"))
	right = float(raw_input("right:"))
	lower = float(raw_input("lower:"))
	upper = float(raw_input("upper:"))

	#
	# The values are scaled to the dimensions specified. The y-axis is reversed.
	#

	datain[:,:,1] = currimg.shape[0] - datain[:,:,1]
	datain[:,:,0] = left + (right-left)*datain[:,:,0]/currimg.shape[1]
	datain[:,:,1] = lower + (upper-lower)*datain[:,:,1]/currimg.shape[0]
	
	#
	# In this loop an extra number of lines are created between the lines specified by the user until the number
	# of values for Pe corresponds to the number of xy-values.
	#
	
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

#
# The "mean-value"-lines are plotted
#
for i in range(len(datain[:,0,0])):
	plt.plot(datain[i,:,0],datain[i,:,1])
	
plt.show()


allx = datain[0,:,0]
allPe = Pe[0,:]

ally = datain[0,:,1]

#
# In this loop, the clicks are put in arrays of the form ([x0,Pe0], [x1,Pe1] ....) and (y0, y1, y2 ....)
#

i=1
while i < len(Pe[:,0]):
	allx = np.append(allx, datain[i,:,0])
	allPe = np.append(allPe, Pe[i,:])
	ally = np.append(ally, datain[i,:,1])
	i = i+1

allpoints = np.array([allx,allPe]).T

# 
# Three different interpolation-methods are used and plotted for the user to see
#

tck1 = interpolate.CloughTocher2DInterpolator(allpoints,ally)
tck2 = interpolate.LinearNDInterpolator(allpoints,ally)
tck3 = interpolate.NearestNDInterpolator(allpoints,ally)
tck = [tck1, tck2, tck3]
x = np.linspace(allx.min(),allx.max(),200)
for j in range(3):
	Peplot = np.linspace(Pe[0,0], Pe[len(Pe)-1,0], 200)

	for i in range(len(Peplot)):
		plt.plot(x,tck[j](x,Peplot[i]))

	for i in range(len(datain[:,0,0])):
		plt.plot(datain[i,:,0],datain[i,:,1],'r+')

	plt.show()
#
# 1 corresponds to the cubic spline-interpolator, 2 to the linear, and 3 to the nearest neighbour-interpolator
#

chosentck = int(raw_input("which one was better? (1,2,3)")) - 1
savefile = str(raw_input("file for saving function variables? (<n> to cancel save):"))
if savefile is not "n":
	pickle.dump(tck[chosentck],open(savefile,'wb'))
	print "saved as ",savefile
