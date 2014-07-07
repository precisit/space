import math
import json

def Ta(rocketdata): 
	data = json.loads(rocketdata)
	t1 = data["m1b"]*data["Isp1SL"]*9.81/data["T1"]
	t2 = data["m2b"]*data["Isp2V"]*9.81/data["T2"]
	Ta = t1 +t2 +ssT
	print "t1", t1
	print "t2", t2
	print "Ta", Ta
	res = json.dumps(Ta)
	return res

def T3s(rocketdata):
	data = json.loads(rocketdata)
	value = 3*(1-math.exp(-0.333*(data["deltaVp"]+1500)/(9.81*data["Isp"])))*9.81*data["Isp"]/data["A0"]
	res = json.dumps(value)
	print "T3s", value
	return res # deltav + 1500

def Tmix(rocketdata):
	TaVal = json.loads( Ta(rocketdata) )
	T3sVal = json.loads( T3s(rocketdata) )
	TmixVal = 0.405*TaVal + 0.595*T3sVal
	T = {"Tmix":TmixVal, "Ta":TaVal, "T3s" : T3sVal}
	Tjson = json.dumps(T)
	return Tjson

#rocket data
Isp1SL = 321
Isp1V = 363
m1wet = 2449399
m1dry = 85729
m1res = 153638
T1 = 40061537.0
m1b = m1wet - m1dry - m1res
	# 
Isp2V = 377
m2wet = 816466
m2dry = 53070
m2res = 1527
T2 = 10430178
m2b = m2wet - m2dry - m2res
mp = 128367
ssT = 0
A0 = T1/(m1wet + m2wet + mp) # + payload!!!!
print "A0", A0

data = {"Isp1SL":Isp1SL, "Isp" : Isp1V, "m1b" : m1b, "T1" : T1, "Isp1V" : Isp1V,
		"m2b" : m2b, "Isp2V" : Isp2V, "T2" : T2, "deltaVp" : 7788, "A0" : A0, "ssT" : ssT}
rocketdata = json.dumps(data)
print Tmix(rocketdata)