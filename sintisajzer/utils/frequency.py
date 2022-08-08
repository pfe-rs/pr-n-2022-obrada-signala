import numpy as np
import librosa
import soundfile as sf

from scipy.io import wavfile

def get_frequency(input, start_time = 0, end_time = 1000):
    sr, data = wavfile.read(input)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]

    N = len(dataToRead)
    yf = np.fft.rfft(dataToRead)
    xf = np.fft.rfftfreq(N, 1 / sr)

    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    return freq

# Cx 
# n_steps 12, Cx -> C(x+1)
# n_steps -12, Cx -> C(x-1)

# N = [ A0, B0, C1, D1, E1, F1, G1 ... B3, C4, D4 ... A7, B7 ] 
# C1, N = 2
# n_steps
# n_steps +1, http://www.phys.unsw.edu.au/jw/notes.html  
def change_pitch_and_write_to_file(input, output, steps):
    y, sample_rate = librosa.load(input, sr=16000)
    y_shifted = librosa.effects.pitch_shift(y, sample_rate, n_steps=steps) # <- n_steps
    sf.write(output, y_shifted, sample_rate, "PCM_24")