import scipy.constants as consts
import atmofunc
import numpy as np
import scipy.constants as consts
import OrbitCalculations as OC
Re = 6371000.
Me = 5.97219e24
We = np.array([0,0,2*np.pi/(24*60*60)])

class Rocket:
	def __init__(self,mw1, md1, mi1, isp1v, isp1sl, thr1sl,
				mw2, md2, mi2, isp2v, thr2v,
				mp, t, nAlt, nT, alim):
		self.t = t
		self.stage1 = True
		self.stage2 = True
		self.cutFuel = False

		self.mw1 = mw1
		self.md1 = md1
		self.mi1 = mi1
		self.isp1v = isp1v
		self.isp1sl = isp1sl
		self.thr1sl = thr1sl

		self.mw2 = mw2
		self.md2 = md2
		self.mi2 = mi2
		self.isp2v = isp2v
		self.thr2v = thr2v

		self.mfuel1 = mw1-mi1-md1
		self.mfuel2 = mw2-mi2-md2
		self.mdot1 = thr1sl/(isp1sl*consts.g)
		self.mdot2 = thr2v/(isp2v*consts.g)
		self.mdot = self.mdot1
		self.mp = mp

		self.nAlt = nAlt
		self.nT = nT
		self.nStartT = None

		self.firstcall = True
		self.initThrust = np.zeros(3)
		self.alim = alim*consts.g

		self.mflow = 1

		self.mcurr = mw1+mw2+mp
		self.Ae1 = atmofunc.Ae(isp1v, self.mdot1, thr1sl)
		self.Ae2 = self.Ae1
		self.Ae = self.Ae1
		self.isp = self.isp1v
		self.mfuelCurrent = self.mfuel1+self.mfuel2

	def SetMass(self,t):
		if self.mfuelCurrent > self.mfuel2:
			self.mfuelCurrent -= (t-self.t)*self.mdot*self.mflow
			self.mcurr = self.mfuelCurrent + self.md1+self.md2+self.mi1+self.mi2+self.mp
		else:
			self.mfuelCurrent -= (t-self.t)*self.mdot*self.mflow
			self.mcurr = self.mfuelCurrent+self.md2+self.mi2+self.mp
				

	def MainController(self, t):
		if self.cutFuel:
			self.mdot = 0
		else:
			if self.mfuelCurrent > self.mfuel2:
				self.mdot = self.mdot1
				self.isp = self.isp1v
			elif self.mfuelCurrent <= 0:
				self.mdot = 0
			else:
				self.mdot = self.mdot2
				self.isp = self.isp2v
				self.Ae = self.Ae2
		self.SetMass(t)
		self.t = t

	def ThrustGravTurn(self, pos, v, t):
		
		alt = np.linalg.norm(pos) - Re
		posUnit = pos/np.linalg.norm(pos)
		vUnit = v/np.linalg.norm(v)
		tangent = np.cross(pos,np.cross(v,pos))
		tangUnit = tangent/np.linalg.norm(tangent)
		apsis = OC.ApsisCalculation(pos,v)

		if apsis[1]>Re+150e3 :
			self.cutFuel=True
			self.mdot = 0
			ThrUnit=posUnit
		else:
			if (alt < self.nAlt):
				ThrUnit = posUnit
				
			elif (self.nStartT is None):
				self.nStartT = t
				ThrUnit = posUnit
				#print "initiate nudge! time, alt",t,alt
			elif (t - self.nStartT < self.nT):
				ThrUnit = tangUnit
				#print "nudging! time, direction",t,ThrUnit
			else:
				ThrUnit = vUnit - Re*np.array([math.cos(lat)*math.cos(longi),
						   math.cos(lat)*math.sin(longi),
						   math.sin(lat)])
		
		
		maxThrust = atmofunc.thrustEff(self.isp,self.Ae,pos,self.mdot) 
		
		return maxThrust*ThrUnit
	def newThrustGravTurn(self, pos, v, t, F):

		alt = np.linalg.norm(pos) - Re
		posUnit = pos/np.linalg.norm(pos)
		vUnit = v/np.linalg.norm(v)
		surfV = atmofunc.inertToSurfVel(v,pos,t)
		surfVUnit = atmofunc.unit(surfV)
		gTurnUnit = atmofunc.surfToInertPos(surfVUnit,t)
		tangent = np.cross(pos,np.cross(v,pos))
		tangUnit = atmofunc.unit(tangent)
		#apsis = OC.ApsisCalculation(pos,v)
		if self.firstcall:
			ThrUnit = np.cos(np.radians(4))*posUnit + np.sin(np.radians(4))*vUnit
			self.firstcall = False
			self.initThrust = ThrUnit
		elif (alt < self.nAlt):
			ThrUnit = self.initThrust
		elif (self.nStartT is None):
			self.nStartT = t
			ThrUnit = gTurnUnit
			#print "initiate nudge! time, alt",t,alt
		elif (t - self.nStartT < self.nT):
			ThrUnit = atmofunc.unit(np.cos(np.radians(45))*tangUnit + np.sin(np.radians(45))*gTurnUnit)
			#print "nudging!", np.linalg.norm(ThrUnit)
		elif  (alt>200000):
			ThrUnit = tangUnit
			if OC.escVel(pos) < np.dot(v,tangUnit) :
				self.cutFuel = True
				self.mdot = 0
				#print "cutFuel"

		else:
			ThrUnit = gTurnUnit



		#if (np.linalg.norm(np.linalg.norm(ThrUnit)-1)>0.00001:
		#	print (np.linalg.norm(np.linalg.norm(ThrUnit)-1)
		self.accLimit(F)
		Thrust = atmofunc.thrustEff(self.isp,self.Ae,pos,self.mdot*self.mflow) 
		return Thrust*ThrUnit

	def accLimit(self,F):
		adif = F/self.mcurr - self.alim
		if (adif < 0):
			self.mflow = 1
		else:
			self.mflow = 1 -adif*self.mcurr/F
			print "mflow",self.mflow


