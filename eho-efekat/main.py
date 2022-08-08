#Biblioteke
import os
import glob

from playsound import playsound
from scipy.io import wavfile

from scipy import signal
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import filedialog, font



#Osnove
root = Tk()
root.title('SignalEho')
root.geometry("400x350")
root.iconbitmap('logo.ico')
root['background']='papaya whip'
Font1 = font.Font(family='Times New Roman')

#Dodatno
imeFajla = ""
brojac = 0

#Recnik
impulsniOdziviFajlovi = {
    "Katedrala": {
        "nazivFajla": "katedrala.wav",
        "skaliranje": 0.4
    },
    "Tunel": {
        "nazivFajla": "tunel.wav",
        "skaliranje": 0.05
    },
    "Amfiteatar": {
        "nazivFajla": "amfiteatar.wav",
        "skaliranje": 0.075
    },
    "Šuma": {
        "nazivFajla": "šuma.wav",
        "skaliranje": 0.7
    },
}

#Odaberi Fajl
def odaberiFajl():
    global imeFajla
    imeFajla = filedialog.askopenfilename(
        initialdir=".",
        title="Odaberi fajl",
        filetypes=(("wav files", "*.wav"), )
    )
    Label(root, text=imeFajla).pack()



odaberiFajlDugme = Button(root, text="Odaberi fajl", command=odaberiFajl, padx= 50, pady=25, fg= "black", bg= "white")
odaberiFajlDugme.pack(side='top')


#Meni
opcije = [
    "Izaberi prostoriju",
    "Katedrala",
    "Tunel",
    "Amfiteatar",
    "Šuma",
]

izabranaOpcija = StringVar()
izabranaOpcija.set(opcije[0])

drop = OptionMenu(root, izabranaOpcija, *opcije)

drop.config(bg="white", fg="green")
drop["menu"].config(bg="white", fg="green")
drop['font'] = Font1
drop['font'] = font.Font(size=15)

drop.pack(ipadx=50, ipady=10, padx=100, pady=50)

#Konvolucija
def pustiZvuk():
    fs, ulazniSignal = wavfile.read(imeFajla)
    ulazniSignal = ulazniSignal.astype('float64')

    argumentiIzabraneOpcije = impulsniOdziviFajlovi[izabranaOpcija.get()]
    nazivFajla = argumentiIzabraneOpcije["nazivFajla"]
    fs, impulsniOdziv = wavfile.read(nazivFajla)

    skaliranje = argumentiIzabraneOpcije["skaliranje"]
    konvoluiranSignal = signal.convolve(ulazniSignal, impulsniOdziv) * skaliranje

    data = konvoluiranSignal.astype('int32')
    global brojac
    brojac += 1
    wavfile.write(f'out{brojac}.wav', fs, data)

    playsound(f'out{brojac}.wav')


#PLOTOVANJE
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(ulazniSignal)
    ax[0].set_title('Signal pre konvolucije')

    ax[1].plot(data)
    ax[1].set_title(f'Signal nakon konvolucije sa {izabranaOpcija.get()}')
    fig.set_size_inches(10, 5)
    plt.tight_layout()
    plt.show()

#Pusti zvuk
pustiZvukDugme = Button(root, text="Poslušaj", command=pustiZvuk, fg= "black", bg= "white" )
odaberiFajlDugme['font'] = Font1
odaberiFajlDugme['font'] = font.Font(size=10)
pustiZvukDugme.pack(ipadx=15, ipady=7)



root.mainloop()

#Brisanje starih fajlova
fileList = glob.glob('out*.wav')
for filePath in fileList:
    try:
        os.remove(filePath)
    except:
        print()