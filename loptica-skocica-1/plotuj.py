import matplotlib.pyplot as plt
import numpy as np

h = np.array([0.5,0.7,1,1.3,1.5])
dots = [0.7985073045800782,0.7472155294991633,0.6855186278759765,0.5989538540752704,0.5486540294954426]

plt.plot(h,dots)
plt.plot(h,-h/4+0.9235)
plt.show()