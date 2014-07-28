import numpy as np
from scipy.integrate import odeint
import atmofunc
import math
import matplotlib.pyplot as plt
import scipy.constants as consts
import RocketClass
import OrbitCalculations as OC
import time as timer
import RocketSim
import warnings
Re = 6371000.
We = np.array([0,0,2*math.pi/(24*60*60)])
lat = math.radians(0) 									# Latitude
longi = math.radians(90)								# Longitude
initPos = Re*np.array([math.cos(lat)*math.cos(longi),
					   math.cos(lat)*math.sin(longi),
					   math.sin(lat)])					# Initial position vector

initVel = np.cross(We, initPos)							# Initial velocity vector
mp = 1000.
initial_conds = [initPos[0], initVel[0], initPos[1], initVel[1], initPos[2], initVel[2],
				 402000 + 90720 + mp, 0, 5885.e3]
time = np.linspace(0,8000,1000) 
def simFunc(nudgeAlt,nudgeTime):

	R = RocketClass.Rocket(402000., 16000., 3900., 320., 280., 5885.e3, 90720., 3200., 182., 345., 800000., mp, time[0], nudgeAlt,nudgeTime,100)
	solutions = odeint(RocketSim.RocketFunc, initial_conds, time, args=(R,))
	return solutions		

if __name__ == '__main__':
	nAlts = np.linspace(10000.,14000.,2)
	nTimes = np.linspace(0.,1.,2)
	print nAlts
	print nTimes
	print len(nTimes)

	succAlts = []
	succTimes = []
	succdeltaV = []
	startTime = timer.time()
	global crash
	for i in range(len(nAlts)):
		for j in range(len(nTimes)):
			
			crash = False
			with warnings.catch_warnings():
   				warnings.simplefilter("ignore")
   				sol = simFunc(nAlts[i],nTimes[j])
			pos = np.array([sol[:,0], sol[:,2], sol[:,4]])
			
			for k in range(len(time)):
				alt = np.linalg.norm(pos[:,k])-Re
				if alt <= -1:
					crash = True
					print "crash"
					break
			
			if not crash:
				succAlts.append(nAlts[i])
				succTimes.append(nTimes[j])
				succdeltaV.append(np.max(sol[:,7]))
				print "SCORE!"
			print i,j

	print "time to execute",timer.time()-startTime
	print "succesful nudgetimes, altitudes and deltaV"
	print succTimes
	print succAlts
	print succdeltaV
	successMat = np.array([succTimes,succAlts,succdeltaV])
	minindex = np.where(succdeltaV == np.min(succdeltaV))
	succesVec = successMat[:,minindex]
	print succesVec


			
				

#pos = np.array([solutions[:,0], solutions[:,2], solutions[:,4]])
#deltaV = solutions[:,7]
