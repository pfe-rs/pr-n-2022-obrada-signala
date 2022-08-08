import scipy
from scipy import signal
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

fs, zvuk = wavfile.read('zvuk_0.9m.wav')

#print(len(zvuk)/fs)
#print (fs)


vrednost1, Grafik1= plt.subplots()
t=np.linspace(0,len(zvuk)/fs,len(zvuk))
Grafik1.plot(t,zvuk)
plt.show()



Niz = zvuk[:,0]
#print (len(Niz))


sum = np.max(Niz)/4

for i in range(len(Niz)):
    if (Niz[i]<sum):
        Niz[i]=0
    else:
         Niz[i]=1

vrednost, Grafik= plt.subplots()
Grafik.plot(t,Niz)
plt.show()


vremena=[]
udarci=[]
for i in range (len(Niz)):
    if (Niz[i]==1):
        vremena.append(i)
    

for i in range(len(vremena)):
    if (i>=1):
        if (vremena[i]-vremena[i-1])<(fs//4):
            udarci.append(i)

#print (udarci)

for i in range(len(udarci)):
    vremena[udarci[i]]=0

trenutak=[]

for i in range(len(vremena)):
    if (vremena[i]!=0):
        trenutak.append(vremena[i])

#print(trenutak)

brzine=[]

for i in range(len(trenutak)):
    if (i==1):
        vr=trenutak[i]
        vr=vr/fs
        brzine.append(vr*9.81/2)
    
    if (i>1  and i<len(trenutak)):
        vr=trenutak[i]-trenutak[i-1]
        vr=vr/fs
        brzine.append((vr*9.81)/2)

#print (brzine)
visina=0

procenti1=(brzine[1]-brzine[2])/brzine[1]
procenti2=(brzine[2]-brzine[3])/brzine[2]
#print(procenti1)
#print(procenti2)
#procenti=(procenti1+procenti2)/2
procenti=0
for i in range (5):
    if (i>=1):
        pr=brzine[i]-brzine[i+1]
        pr=pr/brzine[i]
        procenti=procenti+(brzine[i]-brzine[i+1])/brzine[i]
        #print (pr)

procenti=procenti/(4)

#print("Procenat je")
#print(procenti)

h=(brzine[1]/(1-procenti)*brzine[1]/(1-procenti)/2)/9.81

print("Visina je")
print(h/0.705)