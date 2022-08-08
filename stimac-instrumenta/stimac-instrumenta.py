import numpy as np
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import scipy.io.wavfile as wav

windowSize=44100
all_notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
kamerton = 440

def find_closest_pitch (pitch):
    i = int (np.round(np.log2(pitch/kamerton)*12))
    closest_note= all_notes[i%12] + str(4 + (i+9) // 12)
    closest_pitch = kamerton*2**(i/12)
    return closest_note, closest_pitch

sampleFreq, note = wav.read("example.wav")
niz = abs(fft(note)[:len(note)//2])

for i in range(int(62/(sampleFreq/windowSize))):
    niz[i]=0

maxInd=np.argmax(niz)
maxFreq = maxInd * (sampleFreq/windowSize) 
closestNote, closestPitch = find_closest_pitch(maxFreq)

print(closestNote, closestPitch)