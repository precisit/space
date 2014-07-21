import math
"""
m1b, m2b - Total fuel mass for stage 1 and 2 respectively [kg].
Isp1SL - Specific impulse at sea level for stage 1 [s].
Isp2V - Specific impulse in vacuum for stage 2 [s].
ssT - Stage separation time [s].
"""

# Calculates the total ascention time
def Ta(m1b, Isp1, T1, m2b, Isp2, T2, ssT): 
	t1 = m1b*Isp1*9.81/T1
	t2 = m2b*Isp2*9.81/T2
	return t1 + t2 + ssT

# Calculates the ascention time according to eq.4 in Schilling
def T3s(deltaVp, Isp, A0):
	value = 3*(1-math.exp(-0.333*(deltaVp)/(9.81*Isp)))*9.81*Isp/A0
	return value # deltav + 1500

# Calculates the weighted ascention time according to eq.6 in Schilling
def Tmix(m1b, Isp1SL, T1, m2b, Isp2V, T2, deltaVp, Isp1V, A0, ssT):
	return 0.405*Ta(m1b, Isp1SL, T1, m2b, Isp2V, T2, ssT) + 0.595*T3s(deltaVp, Isp1V, A0)

def rockEq(m01,m11,m02,m12,Isp1,Isp2):
	 deltaV = Isp1*9.81*math.log(m01/m11) + Isp2*9.81*math.log(m02/m12)	
	 return deltaV