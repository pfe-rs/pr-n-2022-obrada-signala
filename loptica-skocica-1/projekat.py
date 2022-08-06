from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.io.wavfile import read
import simpleaudio as sa


fs,data = read('loptica 1.5m 1.wav')
print("done loading")
t = np.linspace(0,len(data)/fs,len(data))
oneChannelData = data[:,0]
print("done one channelling")
fig,ax = plt.subplots()
#ax.plot(t,data)
#plt.show()
border = np.max(oneChannelData)/4
oneChannelData = [0 if oneChannelData_ < border  else 1 for oneChannelData_ in oneChannelData]
print("done clearing useless values")
#ax.plot(t,oneChannelData)
#plt.show()
nonZeroValues = np.nonzero(oneChannelData)
indices=[]
for i in range(1,len(nonZeroValues[0])):
    if (nonZeroValues[0][i]-nonZeroValues[0][i-1])<(fs//5):
        indices.append(i)

print("done finding breaks")
nonZeroValues = np.delete(nonZeroValues,indices)
pauses = []
velocities = []
print(len(nonZeroValues))
for  i in range(len(nonZeroValues)-1):
    pauses.append((nonZeroValues[i+1]-nonZeroValues[i])/fs)
    velocities.append(pauses[i]/2*9.81)
    
print(pauses)
print(velocities)
discriminant = 13.85- 4*2.0225*pow(velocities[0],2)/9.81
if(discriminant>=0):
    h1 = (-3.7214 + sqrt(discriminant))/-2
    print("h ="+ str(round(h1,2))+'m')
else:
    h1real = -3.7214/-2
    h1imag = -sqrt(-discriminant)/-2
    print("h = "+str(round(h1real,2))+" + i" + str(round(h1imag,2)))
    print("|h| ="+str(round(sqrt(pow(h1real,2)+pow(h1imag,2)),2)))

"""
sa.play_buffer(data,1,1,fs)
"""
