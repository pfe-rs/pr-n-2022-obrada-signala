import scipy
from scipy import signal
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from matplotlib import pyplot as plt
import numpy as np
from ipywidgets import interact

#Osnovni parametri modulacije
duration=2
sr=10000
fnosioca=10
m=10
zelimsum=True
#Podesavanja si1gnala
dt = duration/sr
t = np.arange(0,duration,dt)
org=np.sin(2*np.pi*t)+0.8*np.sin(2*np.pi*t*3)

# modulator
novsig = np.zeros(len(org))
#integral=np.cumsum(org)
#novsig=np.sin(2*np.pi*fnosioca*t+m*integral*dt)
integral=0
novsig = np.zeros(len(org))
for i in range(0,len(org)):
    integral+=org[i]*dt
    novsig[i]=np.sin(2*np.pi*fnosioca*t[i]+m*integral)
plt.plot(t,org)
plt.plot(t,novsig)
plt.show()

if zelimsum:
    sum=np.random.rand(len(novsig))
    sum-=0.5
    sum*=0.2
    nfsum=1/np.sqrt(2) + (np.cos(np.pi*t/2)**2)/3 + (np.sin(np.pi*t/7 + np.sqrt(t))**2)/4
    plt.plot(t,novsig)
    plt.plot(t,novsig*nfsum+sum)
    plt.show()
    novsig=novsig*nfsum+sum


# demodulator
demodulacija=np.zeros(len(org))
for i in range(1,len(novsig)):
    if(novsig[i]*novsig[i-1]<=0):
        demodulacija[i]=1
        for j in range(i+1,min(i+11,len(novsig))):
            if(novsig[i-1]*novsig[j]>0):
                demodulacija[i]=0
    else:
        demodulacija[i]=0
plt.plot(t,novsig)
plt.plot(t,demodulacija)
plt.show()
p1=0
p2=0
for i in range(1,len(demodulacija)):
    if demodulacija[i]==1:
        demodulacija[i]=0
        break
for i in range(len(demodulacija)-1,0,-1):
    if demodulacija[i]==1:
        demodulacija[i]=0
        break
while(p2<len(demodulacija)): #Ovo je linearno, iako je petlja u petlji
    while(p2<len(demodulacija)):
        if(demodulacija[p2]==1):
            break
        p2+=1
    if p2==len(demodulacija):
        p2-=1
    raz=p2-p1
    while(p1<=p2):
        demodulacija[p1]=0.5/(raz*dt)
        p1+=1
    p1-=1
    p2+=1
demodulacija-=fnosioca
demodulacija/=(np.pi)*(m/20)
zbir=0
d=500
demodulacija2=np.zeros(len(demodulacija))
for i in range(0,d):
    zbir+=demodulacija[i]
    demodulacija2[i]=zbir/(i+1)
for i in range(d,len(demodulacija)):
    zbir-=demodulacija[i-d]
    zbir+=demodulacija[i]
    demodulacija2[i]=zbir/d
plt.plot(t,novsig)
plt.plot(t,demodulacija)
plt.show()

plt.plot(t,demodulacija)
plt.plot(t,demodulacija2)
plt.show()
plt.plot(t,org)
plt.plot(t,demodulacija2)
plt.show()
