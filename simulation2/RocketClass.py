import scipy.constants as consts
import atmofunc
import numpy as np
import scipy.constants as consts
Re = 6371000
Me = 5.97219e24

class Rocket:
	def __init__(self,mw1, md1, mi1, isp1v, isp1sl, thr1sl,
				mw2, md2, mi2, isp2v, thr2v,
				mp, t, nAlt, nT):
		self.t = t
		self.stage1 = True
		self.stage2 = True
		self.cutFuel = False
		self.reach = False

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

		self.mcurr = mw1+mw2+mp
		self.Ae1 = atmofunc.Ae(isp1v, self.mdot1, thr1sl)
		self.Ae2 = self.Ae1
		self.Ae = self.Ae1
		self.isp = self.isp1v
		self.mfuelCurrent = self.mfuel1+self.mfuel2

	def SetMass(self,t):
		if self.mfuelCurrent > self.mfuel2:
			self.mfuelCurrent -= (t-self.t)*self.mdot
			self.mcurr = self.mfuelCurrent + self.md1+self.md2+self.mi1+self.mi2+self.mp
		else:
			self.mfuelCurrent -= (t-self.t)*self.mdot
			self.mcurr = self.mfuelCurrent+self.md2+self.mi2+self.mp
				

	def MainController(self, t):
		if self.cutFuel or self.reach:
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
		maxThrust = atmofunc.thrustEff(self.isp,self.Ae,pos,self.mdot) 
		alt = np.linalg.norm(pos) - Re
		posUnit = pos/np.linalg.norm(pos)
		vunit = v/np.linalg.norm(v)
		tangent = np.cross(pos,np.cross(v,pos))
		tangUnit = tangent/np.linalg.norm(tangent)
		
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
			ThrUnit = vunit
		escVel = np.sqrt(consts.G*Me/np.linalg.norm(pos))
		beta = np.arccos(np.dot(v,tangent)/(np.linalg.norm(tangent)*np.linalg.norm(v)))
		if (np.linalg.norm(v)>escVel and beta<0.05):
			self.cutFuel = True
			#print "success! maybe... t, alt",t,alt
		elif (self.cutFuel):
			ThrUnit=tangUnit
			self.cutFuel=False
			#print "nudging again!",t,alt

		return maxThrust*ThrUnit