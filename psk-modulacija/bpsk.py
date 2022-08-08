import numpy as np
import matplotlib.pyplot as plt

a = [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0] #digitalni signal koji zelimo poslati


def add_noise(SNR, x, t):
    Ps = np.mean(x ** 2)
    Pn = Ps / 10**(0.1*SNR)
    return x + np.sqrt(Pn) * np.random.randn(len(t))


bitrate = 2000 #broj bitova u sekundi
samplerate = 1000000 #broj sample-ova u sekundi
f = 1 #frekvencija
A = 1 #amplituda
bit_s = 1 / bitrate #trajanje jednog bita u sekundama
samp_bit = int(bit_s * samplerate) #broj sample-ova po bitu


digital = np.repeat(a, samp_bit)
t = np.arange(0, len(a)/bitrate, 1/samplerate)

psk = A * np.sin(2*f*np.pi*(t*bitrate) + np.pi*digital)

#Ukoliko zelimo sum:
#psk = add_noise(-4, psk, t)

demodulated = []
b = A * np.sin(2*np.pi*f*(t*bitrate))
psk2 = psk * b

curr_bit = 0
while curr_bit < len(psk2):
    sub = psk2[curr_bit : curr_bit+samp_bit]
    avg = np.average(sub)
    if avg > 0:
        demodulated.append('0')
    else:
        demodulated.append('1')
    curr_bit = curr_bit + samp_bit
    
print(demodulated)

plt.plot(t, psk)
plt.show()