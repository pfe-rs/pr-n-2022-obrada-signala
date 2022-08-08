# Biblioteke
import os
import sys
import time
import pygame
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from pydub import AudioSegment
os.system('cls')
print("Biblioteke uspješno učitane")
time.sleep(1)
os.system('cls')

# Stavke za pygame
pygame.init()
winSize = (500, 500)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
micL = pygame.image.load("Images\micL.png")
micR = pygame.image.load("Images\micR.png")
micSize = (50, 50)
micL_pos = (160, (winSize[1]//2) - (micSize[1]//2))
micR_pos = (micL_pos[0] + 130, (winSize[1]//2) - (micSize[1]//2))
izv_pos = (winSize[0] // 2, winSize[1] // 2) # Početna kalibrisana pozicija

# Funkcija koja učitava signale iz jednog stereo snimka
def load_signals_fof():
    s1 = str(input("Unesite zvuk sa lijevog mikrofona: "))
    s2 = str(input("Unesite zvuk sa desnog mikrofona: "))
    return wavfile.read(s1)[1][:, 0], wavfile.read(s2)[1][:, 1], s1

# Funkcija koja mjeri vrijeme snimka u sekundama
def wav_len(audioSource):
    audio = AudioSegment.from_file(audioSource)
    return (len(audio) / 1000)

# Funkcija koja traži prvi manji
def first_smaller(arr, amp):
    fsi = 0 # First smaller (index)
    for x in range(0, len(arr)):
        if arr[x] <= amp: fsi = x
    return fsi

def calc_avg_amp(arr):
    av = 0
    for x in arr:
        av += (abs(x) / len(arr))
    return av

# Zavisnost amplitude od udaljenosti
points = np.array([(10, 6478), (40, 3819), (70, 1686), (100, 1463), (130, 335)])
x = points[:,0]
y = points[:,1]
z = np.polyfit(x, y, 3)
f = np.poly1d(z)
x_new = np.linspace(x[0], x[-1], 50)
y_new = f(x_new)

# Glavna funkcija
def main():
    sig1, sig2, src0 = load_signals_fof() # Signal input
    audioLen = wav_len(src0) # Dužina snimka

    print("Pokretanje algoritma")
    r1 = []
    r2 = []
    for x in range(0, len(sig1) - 5000, 5000):
        r1.append(round(x_new[first_smaller(y_new, calc_avg_amp(sig1[x:x+5000]))], 2))
        r2.append(round(x_new[first_smaller(y_new, calc_avg_amp(sig2[x:x+5000]))], 2))
    print("Vizuelizacija spremna")

    #print(r1)
    #print(r2)
    
    # Petlja za iscrtavanje pozicije
    pos_br = 0
    win = pygame.display.set_mode(winSize) # Pokretanje GUI prozora
    pygame.display.set_caption("Stereo sound localisation")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if pos_br > len(r1) - 1:
            time.sleep(1)
            pygame.quit()

        win.fill(WHITE)
        win.blit(micL, micL_pos)
        win.blit(micR, micR_pos)

        pygame.draw.circle(win, BLACK, (micL_pos[0]+25, micL_pos[1]+25), r1[pos_br], 2)
        pygame.draw.circle(win, BLACK, (micR_pos[0]+25, micR_pos[1]+25), r2[pos_br], 2)

        pygame.display.update()

        time.sleep(audioLen / len(r1))
        pos_br += 1

if __name__ == '__main__':
    main()