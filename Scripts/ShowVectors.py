import sys, os
import numpy as np
import matplotlib as plt

dataFldr = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),"Data")
simFldr = os.path.join(dataFldr,"SimDir")
uFldr = os.path.join(simFldr,'uAtSurface')
vFldr = os.path.join(simFldr,'vAtSurface')

uASC = os.path.join(uFldr,'us_1978_02_15_120000.ASC')
vASC = os.path.join(vFldr,'vs_1978_02_15_120000.ASC')

uArr = np.loadtxt(uASC)
vArr = np.loadtxt(vASC)


