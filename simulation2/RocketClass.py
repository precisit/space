import scipy.constants as consts
import atmofunc
class Rocket:
	def __init__(self,mw1, md1, mi1, isp1v, isp1sl, thr1sl,
				mw2, md2, mi2, isp2v, thr2v,
				mp,t):
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

		self.mcurr = mw1+mw2+mp
		self.Ae1 = atmofunc.Ae(isp1v, self.mdot1, thr1sl)
		self.Ae2 = self.Ae1
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
		self.SetMass(t)
		self.t = t
