import matplotlib.pyplot as plt
import numpy as np

x1 = np.arange(0,5000,1)
path = 'INDiid.txt'
f = open(path, 'r+')
y1=np.loadtxt('INDiid.txt', dtype=float)
f.close()
x2 = x1
path = 'INDmild.txt'
f = open(path, 'r+')
y2=np.loadtxt('INDmild.txt', dtype=float)
f.close()
x3 = x1
path = 'INDmarkov.txt'
f = open(path, 'r+')
y3=np.loadtxt('INDmarkov.txt', dtype=float)
f.close()
x4 = x1
path = 'INDperiodic.txt'
f = open(path, 'r+')
y4=np.loadtxt('INDperiodic.txt', dtype=float)
f.close()

plt.plot(x1,y1, label='i.i.d')
plt.plot(x2,y2,"r",  label='mild')
plt.plot(x3,y3,"y",label='ergodic')
plt.plot(x4,y4,"g",label='periodic')
y_label = r'$\frac{\mathbf{U_{i}^{*}}-\mathbf{U_{i}}}{\mathbf{U_{i}^{*}}}$'
plt.ylabel(y_label)
plt.xlabel("Periods")
plt.title("Individual Regret")
#plt.ylabel("‖$\mathbf{p_{t}}$-$\mathbf{p^{*}}$‖")
plt.xlim(0,5000)
plt.ylim(0,0.5)
plt.legend()
plt.grid()
#plt.show()
plt.savefig("Individual Regret 1.jpg",dpi=600)