import matplotlib.pyplot as plt
import numpy as np

x1 = np.arange(0,5000,1)
x1_updated = np.arange(0, 5000, 100)
path = 'ALG2SOCiid.txt'
f = open(path, 'r+')
y1=np.loadtxt('ALG2SOCiid.txt', dtype=float)
f.close()
y1_updated = y1[::100]
x2 = x1
path = 'ALG22SOCiid.txt'
f = open(path, 'r+')
y2=np.loadtxt('ALG22SOCiid.txt', dtype=float)
f.close()
y2_updated = y2[::100]


plt.plot(x1_updated,y1_updated,"bs" ,label='η$_i$$_,$$_t$=1/t')
plt.plot(x1_updated,y2_updated,"ro",  label='η$_i$$_,$$_t$=1/√t')


plt.ylabel(" Fairness Regret")
plt.xlabel("Periods")

plt.xlim(0,5000)
plt.ylim(0,10000)
plt.legend()
plt.grid()
#plt.show()
plt.savefig("ALG2 1.jpg",dpi=1000)

