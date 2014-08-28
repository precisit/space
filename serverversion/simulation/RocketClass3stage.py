import scipy.constants as consts
import atmofunc
import numpy as np
import scipy.constants as consts
import OrbitCalculations as OC

Re = 6371000.
Me = 5.97219e24
We = np.array([0,0,2*np.pi/(24*60*60)])

class Rocket:
	def __init__(self, mp, t, pitchAlt, pitchT, pitchAng,initAng, gmax, tAlt,
				mw1, md1, mi1, isp1v, isp1sl, thr1sl, Aflow,
				mw2=0, md2=0, mi2=0, isp2v=0, thr2v=0,
				mw3=0, md3=0, mi3=0, isp3v=0, thr3v=0, booster=False):

		self.t = t
		self.stage1 = True
		self.stage2 = True
		self.cutFuel = False
		self.booster = booster

		self.mw1 = mw1
		self.md1 = md1
		self.mi1 = mi1
		self.isp1v = isp1v
		self.isp1sl = isp1sl
		self.thr1sl = thr1sl

		self.Aflow = Aflow
		
		self.mw2 = mw2
		self.md2 = md2
		self.mi2 = mi2
		self.isp2v = isp2v
		self.thr2v = thr2v

		self.mw3 = mw3
		self.md3 = md3
		self.mi3 = mi3
		self.thr3v = thr3v
		self.isp3v = isp3v

		self.deltaVreq = 0
		self.timetoApo = 0
		self.tStart = 0

		self.mfuel1 = mw1-mi1-md1
		self.mfuel2 = mw2-mi2-md2
		self.mfuel3 = mw3-mi3-md3
		self.mdot1 = thr1sl/(isp1sl*consts.g)
		if self.mw2 != 0:
			self.mdot2 = thr2v/(isp2v*consts.g)
		self.mdotsave = 0
		if self.mw3 != 0:
			self.mdot3 = thr3v/(isp3v*consts.g)

		self.mdot = self.mdot1
		if self.booster:
			self.mdotb = self.mdot3
			self.ispb = self.isp3v
			self.mb = self.mfuel3
		else:
			self.ispb = 0
			self.mdotb = 0
		self.mdot
		self.mp = mp

		self.pitchAlt = pitchAlt
		self.tAlt=tAlt
		self.pitchT = pitchT
		self.pitchAng = np.radians(pitchAng)
		self.initAng = np.radians(initAng)
		self.nStartT = None

		self.firstcall = True
		self.initThrust = np.zeros(3)
		self.gmax = gmax*consts.g

		self.mflow = 1

		self.mcurr = mw1+mw2+mw3+mp
		self.Ae = atmofunc.Ae(isp1v, self.mdot1, self.thr1sl)
		if mw2 != 0:
			self.Ae2 = atmofunc.Ae(isp2v, self.mdot2, self.thr2v)
		else:	self.Ae2 = 0
		if mw3 != 0:
			self.Ae3 = atmofunc.Ae(isp3v, self.mdot3, self.thr3v)
		else: self.Ae3 = 0
		self.isp = self.isp1v
		self.mfuelCurrent = self.mfuel1+self.mfuel2+self.mfuel3

	def SetMass(self,t):

		if self.booster:
			if self.mfuelCurrent > self.mfuel2:
				if self.mb <= 0:
					self.mdotb = 0
					self.md3 = self.mi3 = 0

				self.mfuelCurrent -= (t-self.t)*(self.mdot+self.mdotb)*self.mflow
				self.mb -= (t-self.t)*self.mdotb*self.mflow
				self.mcurr = self.mfuelCurrent + self.md1+self.md2+self.md3+self.mi1+self.mi2+self.mi3+self.mp

			else:
				self.mfuelCurrent -= (t-self.t)*self.mdot*self.mflow
				self.mcurr = self.mfuelCurrent+self.mi2+self.md2+self.mp
		else:
			if self.mfuelCurrent > self.mfuel2 + self.mfuel3:
				self.mfuelCurrent -= (t-self.t)*self.mdot*self.mflow
				self.mcurr = self.mfuelCurrent + self.md1+self.md2+self.mi1+self.mi2+self.md3+self.mi3+self.mp

			elif self.mfuelCurrent < self.mfuel2+self.mfuel3 and self.mfuelCurrent > self.mfuel3:
				self.mfuelCurrent -= (t-self.t)*self.mdot*self.mflow
				self.mcurr = self.mfuelCurrent+self.md2+self.mi2+self.mi3+self.md3+self.mp

			else:
				self.mfuelCurrent -= (t-self.t)*self.mdot*self.mflow
				self.mcurr = self.mfuelCurrent+self.mi3+self.md3+self.mp	

	def MainController(self, t):
		if self.cutFuel:
			self.mdot = 0
		else:
			if self.mfuelCurrent <= 0:
				self.mdot = 0

			else:
				if self.booster:
			 		if self.mfuelCurrent > self.mfuel2:

						self.mdot = self.mdot1
						self.isp = self.isp1sl

						if self.mb > 0:
							self.ispb = self.isp3v
							self.mdotb = self.mdotb
						else:
							self.ispb = 0
							self.mdotb = 0
					else:
						self.mdot = self.mdot2
						self.isp = self.isp2v
				else:
					if self.mfuelCurrent > self.mfuel2 + self.mfuel3:
						self.mdot = self.mdot1
						self.isp = self.isp1v
					elif self.mfuelCurrent <= self.mfuel2 + self.mfuel3 and self.mfuelCurrent > self.mfuel3:
						self.mdot = self.mdot2
						self.isp = self.isp2v
					elif self.mfuelCurrent <= self.mfuel3:
						self.mdot = self.mdot3
						self.isp = self.isp3v
		self.SetMass(t)
		self.t = t

	
	def thrustGravTurn(self, pos, v,t, F):

		alt = np.linalg.norm(pos) - Re
		posUnit = pos/np.linalg.norm(pos)
		vUnit = v/np.linalg.norm(v)
		surfV = atmofunc.inertToSurfVel(v,pos)
		surfVUnit = atmofunc.unit(surfV)
		gTurnUnit = surfVUnit#atmofunc.surfToInertPos(surfVUnit,t)
		tangent = np.cross(pos,np.cross(v,pos))
		tangUnit = atmofunc.unit(tangent)
		#apsis = OC.ApsisCalculation(pos,v)
		if self.firstcall:
			ThrUnit = atmofunc.unit(np.cos(self.initAng)*posUnit + np.sin(self.initAng)*vUnit)
			self.firstcall = False
			self.initThrust = ThrUnit
		elif (alt < self.pitchAlt):
			ThrUnit = self.initThrust
		elif (self.nStartT is None):
			self.nStartT = t
			ThrUnit = gTurnUnit
			#print "initiate nudge! time, alt",t,alt
		elif (t - self.nStartT < self.pitchT):
			ThrUnit = atmofunc.unit(np.cos(self.pitchAng)*tangUnit + np.sin(self.pitchAng)*gTurnUnit)
			#print "nudging!", np.linalg.norm(ThrUnit)
		elif  (alt>self.tAlt):
			ThrUnit = tangUnit
			if OC.GetOrbitSpeed(pos) < np.dot(v,tangUnit) :
				self.cutFuel = True
				self.mdot = 0
				#print "cutFuel"
		else:
			ThrUnit = gTurnUnit

		self.accLimit(F)
		Thrust = atmofunc.thrustEff(self.isp,self.Ae,pos,self.mdot*self.mflow, self.isp3v, self.mdotb, self.Ae3) 
		return Thrust*ThrUnit

	def ThrustAlgorithm(self, pos, vel):
		altitude = np.linalg.norm(pos)-Re
		if np.linalg.norm(vel) != 0:
			apoapsis = OC.ApsisCalculation(pos, vel)[1]
		else:
			apoapsis = 0
		
		if apoapsis-Re >= self.tAlt:
			print apoapsis
			horizonVector = np.cross(pos,np.cross(vel,pos))
			ThrUnit = atmofunc.unit(horizonVector)
			self.cutFuel=True
			# Coasting to apoapsis
		else:
			#print OC.FlightPathAngle(self, altitude), altitude
			FPA = np.radians(OC.FlightPathAngle(self, altitude)) #Flight path angle
			horizonVector = np.cross(pos,np.cross(vel,pos))
			horizonUnitVector = atmofunc.unit(horizonVector)
			positionUnitVector = atmofunc.unit(pos)

			ThrUnit = np.cos(FPA)*horizonUnitVector + np.sin(FPA)*positionUnitVector

		Thrust = atmofunc.thrustEff(self.isp,self.Ae,pos,self.mdot*self.mflow, self.isp3v, self.mdotb, self.Ae3)

		return Thrust*ThrUnit


	def accLimit(self,F):
		adif = F/self.mcurr - self.gmax
		if (adif < 0):
			self.mflow = 1
		else:
			self.mflow = 1 -adif*self.mcurr/F


def CreateRocket(param):
	if param['rocket'] == 'falcon9':
		rocket = Rocket(param['payload'], 0, param['pitchAlt'], param['pitchT'], param['pitchAng'], param['initAng'], param['gmax'], param['tAlt'],
						402000., 16000., 3900., 320., 280., 5885.e3, 21.237, # Area med payload fairing
						90720., 3200., 182., 345, 800e3 )
	elif param['rocket'] == 'saturnv':
		rocket = Rocket(param['payload'], 0, param['pitchAlt'], param['pitchT'], param['pitchAng'], param['initAng'], param['gmax'], param['tAlt'],
							2286217, 135218, 0, 304, 265, 38703000, 113,
							490778, 39048, 0, 421, 5.17e6, 
							119900, 13300, 0, 421, 1.03e6, False)
	elif param['rocket'] == 'ariane5':
		rocket = Rocket(param['payload'], 0, param['pitchAlt'], param['pitchT'], param['pitchAng'], param['initAng'], param['gmax'], param['tAlt'],
							170800, 1.27e4, 0, 430, 340, 1.1114e6, 22.9, #Arean utan boosters
						   	1.25e4, 2.7e3,  0, 324, 2.24e4, 
						  	555000, 79600, 0, 275, 2*6.47e6, True)
	elif param['rocket'] == 'soyuz2b':
		rocket = Rocket(param['payload'], 0, param['pitchAlt'], param['pitchT'], param['pitchAng'], param['initAng'], param['gmax'], param['tAlt'],
							105400, 6875, 0, 311, 245, 9.99e5, 22,	  # ungefar samma som falcon 9 med payload fairing
						   	25200, 2355,  0, 359, 2.94e5, 
						  	177600, 15240, 0, 310, 4084000, True)
	elif param['rocket'] == 'atlasv':
		rocket = Rocket(param['payload'], 0, param['pitchAlt'], param['pitchT'], param['pitchAng'], param['initAng'], param['gmax'], param['tAlt'],
							306914, 22461, 0, 338, 253, 4.1e6, 11.4, 	  #Area utan boosters
						   	22825, 2026,  0, 451, 9.9e4, 
						  	81648, 8000, 0, 310, 2.54e6, True)
	elif param['rocket'] == 'custom':
		stats = {'mw2':0, 'md2':0, 'mi2':0, 'isp2v':0, 'thr2v':0, 'mw3':0, 'md3':0, 'mi3':0, 'isp3v':0, 'thr3v':0, 'booster':False}
		stats.update(param['stats'])

		rocket = Rocket(param['payload'], 0, param['pitchAlt'], param['pitchT'], param['pitchAng'], param['initAng'], param['gmax'], param['tAlt'],
						stats['mw1'], stats['md1'], stats['mi1'], stats['isp1v'], stats['isp1sl'], stats['thr1sl'],stats['Aflow'],
						stats['mw2'], stats['md2'], stats['mi2'], stats['isp2v'], stats['thr2v'],
						stats['mw3'], stats['md3'], stats['mi3'], stats['isp3v'], stats['thr3v'], stats['booster'])
	return rocket
