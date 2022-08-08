import scipy
from scipy import signal
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

fs, x = wavfile.read('furElise.wav')

def plotuj(x, fs):
    t = np.linspace(0, len(x) / fs, len(x))
    fig, ax = plt.subplots(figsize = (9, 6))
    plt.plot(t, x)
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.title("Prikaz signala x(t)")
    plt.show()

def plotujf(yf, fs):
    N = len(yf)
    T = 1.0 / fs
    xf = np.linspace(0.0, 1.0/(2.0*T), N)
    fig, ax = plt.subplots()
    ax.plot(xf, 1.0/N * yf)
    plt.show()

def getFFT(x):
    return np.abs(scipy.fft.fft(x)[:len(x)//2])

w = 8820
f = []
for i in range(int(len(x)/w)): #fs/w
    y = x[i*w:(i+1)*w-1,0]
    #plotuj(y, fs)
    yf = getFFT(y)
    #plotujf(yf, fs)
    maxI = 0
    maxV = 0
    for j in range(len(yf)):
        if(yf[j] > maxV):
            maxV = yf[j]
            maxI = j
    f.append(maxI)
for i in range(len(f)):
    f[i] = f[i]*fs/(2*len(yf))

notes = []
for i in range(len(f)):
    note = np.round(12*np.log(f[i]/55)/np.log(2)+33)
    #note = (12*np.log(f[i]/55))/np.log(2)+33
    notes.append(note)
#    print(note)
notesv = [] # notes, velocity
prev = notes[0]
br = 1
for i in range(1, len(notes)):
    if notes[i] != prev:
        notesv.append([prev, br])
        br = 1
        prev = notes[i]
    else:
        br += 1
#for i in range(len(notesv)):
#    print(notesv[i])

#file = open("midifajl1.midi", "rb")

#### 4b MThd, 4b header length, 2b mode (0 - single track), 2b num of track chunks, 2b division
headerChunk = [77, 84, 104, 100, 0, 0, 0, 6, 0, 1, 0, 2, 1, 128]
headerChunkData = bytearray(headerChunk) # header data

trackChunkData0 = bytearray([77, 84, 114, 107, 0, 0, 0, 19,
    0, 255, 88, 4, 4, 2, 24, 8, 0, 255, 81, 3, 6, 187, 88, 0, 255, 47, 0])

eventChunksData = bytearray([])
noteOn = 0x90
noteOff = 0x80
reset = 0xff
for i in range(len(notesv)):
    note = notesv[i][0]
    if(note < 0 or note > 255):
        continue
    message = bytearray([noteOn, int(note), 50, 96])
    eventChunksData += message
    message = bytearray([noteOff, int(note), 0, 0])
    eventChunksData += message

y1, y2, y3, y4 = ((len(eventChunksData)+25) & 0xFFFFFFFF).to_bytes(4, 'big')
trackChunk = [77, 84, 114, 107, y1, y2, y3, y4, 0, 255, 3, 14,
    69, 108, 101, 99, 116, 114, 105, 99, 32, 80, 105, 97, 110, 111, 0, 192, 0, 96]
trackChunkData = bytearray(trackChunk)

with open("track.midi", "wb") as binary_file:
    binary_file.write(headerChunkData + trackChunkData0 + trackChunkData + eventChunksData + bytearray([0xff, 47, 0]))

print('done')


