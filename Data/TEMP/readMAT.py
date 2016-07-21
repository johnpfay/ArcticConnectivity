#To get h5py:
# download wheel from http://www.lfd.uci.edu/~gohlke/pythonlibs/
# pip install <location of download>

import numpy as np
import h5py
import scipy.io as sio

fn = "reefs.mat"
f = sio.matlab.loadmat(fn)

water = f['water']          #
mstruct = f['mstruct']
reefProps = f['reefProps']
reefIDs = f['reefIDs']