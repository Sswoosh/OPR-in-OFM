import matplotlib.pyplot as plt
import numpy as np

x1 = np.arange(0,5000,1)
x2 = x1
path = '10x15SOCiid.txt'
f = open(path, 'r+')
y2=np.loadtxt('10x15SOCiid.txt', dtype=float)
f.close()
x3 = x1
path = '10x20SOCiid.txt'
f = open(path, 'r+')
y3=np.loadtxt('10x20SOCiid.txt', dtype=float)
f.close()
x4 = x1
path = '15x20SOCiid.txt'
f = open(path, 'r+')
y4=np.loadtxt('15x20SOCiid.txt', dtype=float)
f.close()
x5 = x1
path = '20x25SOCiid.txt'
f = open(path, 'r+')
y5=np.loadtxt('20x25SOCiid.txt', dtype=float)
f.close()
x6 = x1
path = 'SOCiid.txt'
f = open(path, 'r+')
y6=np.loadtxt('SOCiid.txt', dtype=float)
f.close()

plt.plot(x2,y2,"r",  label='10*15')
plt.plot(x3,y3,"y",label='10*20')
plt.plot(x4,y4,"b",label='15*20')
plt.plot(x5,y5,"c",label='20*25')
plt.plot(x6,y6,"g",label='20*30')
plt.ylabel("Fairness Regret")
plt.xlabel("Periods")


plt.xlim(0,5000)
plt.ylim(0,5)
plt.legend()
plt.grid()
plt.show()
#plt.savefig("Fairness Regret.jpg",dpi=600)

