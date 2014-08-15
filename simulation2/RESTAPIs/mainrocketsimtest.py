import mainrocketsim as mr
import matplotlib.pyplot as plt
Re = 6371000.
param = {'rocket':'falcon9', 'payload':10000, 'lat':28, 'tAlt':200000, 'optional':{'draglosses':True, 'thrust':True, 'gravlosses':True}}
param1 = {'rocket':'custom', 'payload':10000, 'lat':0, 'longi':213 ,'tAlt':200000, 'optional':{'draglosses':True, 'thrust':True, 'gravlosses':True}}
param2 = {'rocket':'saturnV', 'payload':40000, 'lat':0, 'longi':45, 'tAlt':400000}
param1['stats'] = {'mw1':100000, 'md1':10000, 'mi1':500, 'isp1v':320, 'isp1sl':300, 'thr1sl':2000000}
data=mr.RocketSimulator(param2)


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
circ = plt.Circle((0,0), radius=Re, color='b')
ax.add_patch(circ)
plt.plot(data[0][0], data[0][1])
plt.show()

print data[4], data[5]