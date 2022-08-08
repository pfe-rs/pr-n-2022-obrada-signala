import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import scipy.fft as fft


maxlen = 300000
maxnwin=400
nfreq = 500 #za FFT
nmel=40
firstmfccfactor=1 #predstavlja vaznost prvog koeficijenta jer su amplitude primetno vece od ostatlih koeficijenata



def fromstereo(ax): #neki wav fajlovi su u stereo obliku, ovo ih prevodi u array
    return ax[:,0]
def readsignal(st):
    freq,x = wavfile.read(st)
    if(len(np.shape(x))==2): x = fromstereo(x)
    return freq,np.pad(x, pad_width=(0, maxlen-len(x)), mode='constant'),len(x)
def h2m(a):
    return 1125*np.log(1+a/700)
def m2h(a):
    return 700*(np.exp(a/1125)-1)
def init_melscale(): #pravi trougaone filtre
    lf=h2m(300)
    hf=h2m(8000)
    n=nmel
    r=np.linspace(lf,hf,n+2,dtype=np.intc)
    r = np.intc(np.floor(m2h(r)*(nfreq/22100)))
    mf = np.zeros((nfreq,n)) 
    
    for i in range(n):
        mf[r[i]:r[i+1],i]=np.linspace(0,1,r[i+1]-r[i])
        mf[r[i+1]:r[i+2],i]=np.linspace(1,0,r[i+2]-r[i+1])
    '''
    mf[r[0:n]:r[1:(n+1)],0:n]=np.linspace(0,1,r[1:(n+1)]-r[0:n])
    mf[r[1:(n+1)]:r[2:(n+2)],0:n]=np.linspace(1,0,r[2:(n+2)]-r[1:(n+1)])
    '''
    plt.plot(mf[0:200])
    plt.show()
    return mf

fil=init_melscale()

def normvolume(x): #za utisavanje/pojacavanje
    maxvolume=np.max(x)
    if(maxvolume>40000):  
        x*=(40000//maxvolume)
    return x
def odsecitisinu(x): #za snimak hotworda
    nx=len(x)
    cutoff=500
    for i in range(0,nx):
        if(x[i]>cutoff or x[i]<-cutoff):
             pocetak=i
             break
    for i in range(1,nx):
        if(x[nx-i]>cutoff or x[nx-i]<-cutoff):
             kraj=nx-i
             break
    
    return x[pocetak:kraj]

def f1(x,freq,xlen): #racuna MFC i vraca matricu
    x=normvolume(x)
    n = xlen
    wlen=freq//50 #duzina prozora
    nwin=n//wlen #broj prozora
    wins = np.zeros((nwin,wlen))
    for i in range(0,nwin):
        wins[i]=x[i*wlen : (i+1)*wlen]
    fftspectrum = np.zeros((nwin,nfreq))
    fftspectrum=abs(fft.fft(wins,2*nfreq))[:,0:nfreq] #uradjen FFT
    energy=np.zeros((nwin,nmel))
    np.matmul(fftspectrum,fil,energy) #mnozenje matrica
    energy+=0.001 #zbog loga
    energy=np.log(energy)
    mfc=np.zeros((nwin,nmel//2))
    mfc=fft.dct(energy)[:,1:(nmel//2)+1] #nulti koeficijent je mnogo veci od svih ostalih pa se izostavlja
    plt.imshow(np.transpose(mfc)[::-1], aspect=5)
    plt.show()
    return mfc, nwin

def dtwcost(th,tx):
    return np.sqrt(firstmfccfactor*(th[0]-tx[0])*(th[0]-tx[0]) + np.dot((th-tx)[1:],(th-tx)[1:]))-25 #oduzima se 25 da bi u DTW matrici slicni MFC-evi davali razdaljinu pribliznu nuli

#kontinualni dtw koji trazi hotword HW u signalu X
def dtw2(hwmfc,hwnwin,xmfc,xnwin,xsecs,dtwcutoff):
    d = np.full((hwnwin,xnwin),np.inf) #matrica
    for i in range(xnwin):
        d[0,i]=dtwcost(hwmfc[0],xmfc[i])
    th=np.zeros(nmel//2)
    tx=np.zeros(nmel//2)
    lasts=False
    horc=0
    costs = np.zeros((xnwin-1)*(hwnwin-1),dtype=np.float16)
    cq=0
    for i in range(1,xnwin):
        for j in range(1,hwnwin):
            th=hwmfc[j]
            tx=xmfc[i]
            tcost=dtwcost(th,tx) #norma
            costs[cq]=tcost
            cq+=1
            d[j,i]=tcost+np.amin([d[j,i-1],d[j-1,i],d[j-1,i-1]]) #.......................
            if(d[j,i]==tcost+d[j-1,i-1]): horc+=1
        if(lasts==False and d[hwnwin-1,i]<dtwcutoff):
            #trazenje pocetka:
            ii=i
            jj=j
            route=np.zeros((xnwin+hwnwin,2),dtype=np.float32)
            rc=0
            while(jj!=0 and ii!=0):
                th=hwmfc[jj]
                tx=xmfc[ii]
                p=d[jj,ii]-dtwcost(th,tx)
                route[rc,0]=ii
                route[rc,1]=jj
                rc+=1 #krsh
                if(np.abs(d[jj,ii-1]-p)<0.0001):
                    ii-=1
                elif(np.abs(d[jj-1,ii-1]-p)<0.0001):
                    jj-=1
                    ii-=1
                elif(np.abs(d[jj-1,ii]-p)<0.0001):
                    jj-=1
                else: 
                    print('??',ii,jj)
                    break
            print('Hotword je detektovan od', xsecs*ii/xnwin, 'do', xsecs*i/xnwin, 'sekundi')
            lasts=True
        elif(lasts==True and d[hwnwin-1,i]>dtwcutoff*1.4):
            lasts=False
    #plt.plot(d[hwnwin-1])
    plt.imshow(d[::-1])
    plt.show()
    return

def process(filenames,dtwcutoff):
    nsig=len(filenames)-1
    sigfreqs=np.zeros(nsig, np.intc)
    siglens = np.zeros(nsig, np.intc)
    sigs=np.zeros((nsig,maxlen),np.intc)

    hwfreq, hw, hwlen = readsignal(filenames[0])
    for i in range(nsig):
        sigfreqs[i],sigs[i],siglens[i] = readsignal(filenames[i+1])
    hw=odsecitisinu(hw)                                                                                                                                        
    hwmfc,hwnwin = f1(hw,hwfreq,len(hw))
    signwin = np.zeros(nsig, np.intc)
    sigmfcs=np.zeros((nsig,maxnwin,nmel//2))
    for i in range(nsig):
        tym,signwin[i] = f1(sigs[i],sigfreqs[i],siglens[i])
        sigmfcs[i]=np.pad(tym,pad_width=[(0,(int)(maxnwin-signwin[i])),(0,0)], mode='constant')

    for i in range(nsig):
        print('Snimak',i+1,':')
        dtw2(hwmfc,hwnwin,sigmfcs[i],signwin[i],siglens[i]/sigfreqs[i],dtwcutoff)
    return

filenames1=['hotword_detekcija/hotword.wav',
'hotword_detekcija/primer_1.wav',
'hotword_detekcija/primer_2.wav']

process(filenames1,140)
#process(filenames2,190)