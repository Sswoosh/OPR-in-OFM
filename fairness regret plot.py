import matplotlib.pyplot as plt
import numpy as np

x1 = np.arange(0,5000,1)
x1_updated = np.arange(0, 5000, 100)
path = 'SOCiid.txt'
f = open(path, 'r+')
y1=np.loadtxt('SOCiid.txt', dtype=float)
f.close()
y1_updated = y1[::100]
x2 = x1
path = 'SOCmild.txt'
f = open(path, 'r+')
y2=np.loadtxt('SOCmild.txt', dtype=float)
f.close()
y2_updated = y2[::100]
x3 = x1
path = 'SOCmarkov.txt'
f = open(path, 'r+')
y3=np.loadtxt('SOCmarkov.txt', dtype=float)
f.close()
y3_updated = y3[::100]
x4 = x1
path = 'SOCperiodic.txt'
f = open(path, 'r+')
y4=np.loadtxt('SOCperiodic.txt', dtype=float)
f.close()
y4_updated = y4[::100]

plt.plot(x1_updated,y1_updated,"bs" ,label='iid')
plt.plot(x1_updated,y2_updated,"ro",  label='mild')
plt.plot(x1_updated,y3_updated,"yh",label='ergodic')
plt.plot(x1_updated,y4_updated,"g*",label='periodic')

plt.ylabel(" Fairness Regret")
plt.xlabel("Periods")

plt.xlim(0,5000)
plt.ylim(0,10)
plt.legend()
plt.grid()
#plt.show()
plt.savefig("Social Regret 21.jpg",dpi=600)

