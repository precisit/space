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
	#plt.plot(datain[0,:,0],datain[0,:,1],datain[1,:,0],datain[1,:,1],datain[2,:,0],datain[2,:,1])
plt.show()

#grid_x, grid_Pe = np.mgrid[left:right:numClicks*1j, Pe[0,0]:Pe[len(Pe[:,0])-1,0]:numClicks*1j]
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
#print np.shape(grid_Pe)
#print np.shape(grid_x)
#print np.shape(allpoints)
#print allpoints

#grid_y = interpolate.griddata(allpoints, ally, (grid_x,grid_Pe), method='linear')
"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(allx,allPe,ally)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(grid_x,grid_Pe,grid_y)
plt.show()
"""
tck = interpolate.CloughTocher2DInterpolator(allpoints,ally)
#xND = np.linspace(left,right,200)
#PeND = np.linspace(Pe[0,0],Pe[len(Pe[:,0])-1,0],200)
#yND = tck(np.array([grid_x,grid_Pe]).T)
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(grid_x,grid_Pe,yND)
#plt.show()

"""
ix = np.zeros(np.shape(Pe))
iy = np.zeros(np.shape(Pe))
for i in range(len(Pe[:,0])):
	tck1d = interpolate.interp1d(datain[i,:,0],datain[i,:,1])
	ix[i,:] = np.linspace(datain[:,:,0].min()+0.5, datain[:,:,0].max()-0.5, numClicks)
	iy[i,:] = tck1d(ix[i])

plt.plot(ix[0,:],iy[0,:],ix[1,:],iy[1,:],ix[2,:],iy[2,:])
plt.show()
"""
#tck = interpolate.interp2d(datain[:,:,0], Pe, datain[:,:,1], bounds_error=True, kind = 'linear')
#tck = interpolate.interp2d(grid_x, grid_Pe, grid_y, bounds_error=True, kind = 'linear')

x= np.linspace(allx.min(),allx.max(),200)
#currimg = mpimg.imread("OK-R.png")
"""
y1 = interpolate.bisplev(x,Pe[0,0]*np.ones(np.shape(x)),tck)
y2 = interpolate.bisplev(x,Pe[1,0]*np.ones(np.shape(x)),tck)
y3 = interpolate.bisplev(x,Pe[2,0]*np.ones(np.shape(x)),tck)
y4 = interpolate.bisplev(x,(Pe[2,0]-Pe[1,0])*0.5*np.ones(np.shape(x)),tck)
y5 = interpolate.bisplev(x,(Pe[1,0]-Pe[0,0])*0.5*np.ones(np.shape(x)),tck)

plt.plot(x,y1,x,y2,x,y3,x,y4,x,y5)
"""
plt.plot(x,tck(x,0.101))
plt.plot(x,tck(x,0.65))
plt.plot(x,tck(x,0.2))
plt.plot(x,tck(x,0.99))

for i in range(len(datain[:,0,0])):
	plt.plot(datain[i,:,0],datain[i,:,1],'r+')
#plt.plot(datain[0,:,0],datain[0,:,1],'r+')
#plt.plot(datain[1,:,0],datain[1,:,1],'r+')
#plt.plot(datain[2,:,0],datain[2,:,1],'r+')
#plt.imshow(currimg)
plt.show()

savefile = str(raw_input("file for saving function variables? (<n> to cancel save):"))
if savefile is not "n":
	pickle.dump(tck,open(savefile,'wb'))
	print "saved as ",savefile


"""
pts1OMR[:,0] = left + (right-left)*pts1OMRraw[:,0]/currimg.shape[1]
pts1OMR[:,1] = lower + (upper-lower)*pts1OMRraw[:,1]/currimg.shape[0]
axis([left, right, lower, upper])
plt.plot(pts1OMR[:,0],pts1OMR[:,1])
plt.show()
"""