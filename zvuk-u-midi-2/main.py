import numpy as np
from matplotlib import pyplot as plt 
from scipy.io import wavfile
from midiutil import MIDIFile
from random import randint

def converToMIDI(inputFileName):
    outputFileName = inputFileName[:inputFileName.find('.')] + f"-{randint(100,1000)}" + ".mid"
    outputFile = MIDIFile(1)
    sr, raw_x = wavfile.read(inputFileName)
    x = np.abs(raw_x)
    thresh = max(x) * 0.7

    # detekcija pauza
    pauze = []
    canSwitch = True
    counter = 0
    countVal = 1600
    for index,amp in enumerate(x):
        if counter < countVal and amp > thresh // 10:
            counter = 0
        
        if amp > thresh // 10 and canSwitch:
            canSwitch = False
            pauze.append(index)
            counter = 0

        if counter < countVal and amp <= thresh // 10:
            counter += 1
        
        if counter >= countVal and amp <= thresh // 10 and not canSwitch:
            canSwitch = True
            pauze.append(index)
        
        counter += 1

    print(pauze)

    # prolazenje kroz originalni zapis
    # nota po nota
    # detekcija frekvencija pomocu FFT-a
    notes_raw = []
    timings = []
    for i in range(len(pauze)):
        maxA = 0
        f = 0
        if i + 1 >= len(pauze):
            continue

        interval = raw_x[pauze[i-1]:pauze[i]]

        if len(interval)/sr < 0.05:
            continue

        amps = np.abs(np.fft.fft(interval))
        freqs = np.abs(np.fft.fftfreq(interval.size, d=1/sr))
        
        for amp, freq in zip(amps, freqs):
            if amp > maxA:
                maxA = amp
                f = freq
        
        notes_raw.append(-1)
        notes_raw.append(f)
        timings.append(np.abs((pauze[i+1]-pauze[i])/sr))
        timings.append(len(interval)/sr)
    
    # konverzija frekvencija u MIDI note
    notes = []
    for fnote in notes_raw:
        if fnote == -1:
            notes.append(-1)
        else:
            notes.append(int(np.round(np.log2(fnote/440)*12 + 69)))
    ctime = 0
    for i,note in enumerate(notes):
        if note == -1:
            outputFile.addNote(0, 0, 21, ctime, timings[i], 0)
        else:
            outputFile.addNote(0, 0, note, ctime, timings[i], 127)
        ctime += timings[i]

    # kreiranje samog MIDI fajla
    with open(outputFileName, "wb") as f:
        outputFile.writeFile(f)

    return outputFileName


if __name__ == "__main__":
    # inputFileName = input("Unesite ime fajla u kom se nalazi pesma:")
    print(converToMIDI("very_simple_1ch.wav"))
