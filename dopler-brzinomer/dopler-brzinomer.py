import codeop
import scipy
from scipy import signal
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

fs, x = wavfile.read('doppler.wav')
N = len(x)


fouriers = fft(x[:N//2])
f = np.linspace(0, fs // 2, len(fouriers) // 2)

freqs = np.abs(fouriers)[:len(f)]
freq_max = np.argmax(freqs)
f_dol=f[freq_max]
print(f_dol)


fouriers2 = fft(x[N//2:])
f2 = np.linspace(0, fs//2, len(fouriers2) // 2)

freqs2 = np.abs(fouriers2)[:len(f2)]
freq_max2 = np.argmax(freqs2)
f_odl=f2[freq_max2]
print(f_odl)


v=0
brzina_zvuka=343
v=(brzina_zvuka*(f_dol-f_odl)/(f_dol+f_odl))
v=abs(v)
v=round(v,2)
print(v,'m/s')