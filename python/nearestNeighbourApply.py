#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 18:27:18 2018

@author: jckchow
"""


# -*- coding: utf-8 -*-
"""
/////////////////////////////////////////////////////////////////////////////
//
//   Project/Path:      %M%
//   Last Change Set:   %L% (%G% %U%)
//
/////////////////////////////////////////////////////////////////////////////
//
//   COPYRIGHT Vusion Technologies, all rights reserved.
//
//   No part of this software may be reproduced or modified in any
//   form or by any means - electronic, mechanical, photocopying,
//   recording, or otherwise - without the prior written consent of
//   Vusion Technologies.
//

@author: jacky.chow
"""
import numpy as np
from time import time
from sklearn import neighbors
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib.mlab import griddata
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.colors import ListedColormap

##################################
### User defined parameters
##################################   
#inputFilename  = '/home/jckchow/BundleAdjustment/build/image.jck'
#phoFilename = '/home/jckchow/BundleAdjustment/Data/Dcs28mmTemp.pho'
#iopFilename = '/home/jckchow/BundleAdjustment/Data/Dcs28mm.iop'
#eopFilename = '/home/jckchow/BundleAdjustment/Data/Dcs28mm.eop'

phoFilename = '/home/jckchow/BundleAdjustment/xrayData1/xray1Training.pho'
eopFilename = '/home/jckchow/BundleAdjustment/xrayData1/xray1Training.eop'
outputFilename = '/home/jckchow/BundleAdjustment/xrayData1/Training270Testing30/After/xray1TrainingCalibrated.pho'

##########################################
### read in the residuals output from bundle adjustment
# x, y, v_x, v_y, redu_x, redu_y, vStdDev_x, vStdDev_y
##########################################
eop = np.genfromtxt(eopFilename, delimiter=' ', skip_header=0, usecols = (0,1)).astype(int)
pho = np.genfromtxt(phoFilename, delimiter=' ', skip_header=0, usecols = (0,1,2,3,4,5,6,7))

##########################################
### Apply calibraiton parameters
##########################################

sensorsUnique = np.unique(eop[:,1])

cost = 0.0
numSamples = 0.0
errors = []
outputCost = []
##########################################
### Predicting per sensor
##########################################
for iter in range(0,len(sensorsUnique)): # iterate and calibrate each sensor
    
    sensorCost = 0.0
    avgSensorCost = 0.0
    
    sensorID = sensorsUnique[iter] #currently sensor ID
    indexEOP = np.argwhere(eop[:,1] == sensorID) # eop of the current sensor

    print "Processing sensor: ", sensorID
    
    reg = joblib.load("/home/jckchow/BundleAdjustment/xrayData1/Training270Testing30/NNModel" + str(sensorID.astype(int)) + ".pkl")
    
    #########################################
    ### Predicting per eop
    ##########################################
    for iteration in range(0,len(indexEOP)):        
        eopID = eop[indexEOP[iteration],0]
        
        print "  Processing eop: ", eopID

        indexPho = np.argwhere(pho[:,1] == eopID)
        labels = reg.predict(pho[indexPho,(2,3)])
        
        pho[indexPho, (6,7)] = labels

############################
### Output predicted corrections
############################

np.savetxt(outputFilename, pho, '%i %i %f %f %f %f %f %f', delimiter=' ', newline='\n')
print "Program Succcessful ^-^"