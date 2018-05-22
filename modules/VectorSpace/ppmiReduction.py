import sys
sys.dont_write_bytecode = True

import pandas as pd
import math
import numpy as np


def ppmiReduction(inputPath, folds):
    dataframe = pd.read_csv(inputPath+'/ppmi_1.csv')
    Columns = np.zeros(len(dataframe.columns)-1)
    print Columns
    #After these loops, any Columns[x] with entry = 0 is garbage
    for current in range (1,folds+1):
        dataframe = pd.read_csv(inputPath + '/ppmi_'+str(current)+'.csv')
        numCols = len(dataframe.columns)
        numRows = len(dataframe)
        Matrix = dataframe.as_matrix()
        #print Matrix
        for i in range (0,numRows):
            for j in range (1,numCols):
                if Matrix[i][j] != 0:
                    Columns[j-1] = 1
        #print inputPath + '/ppmi_'+str(current)+'.csv'
    '''
    #this for loop is just for debugging purposes
    for x in range(0,numCols-1):
        if Columns[x] == 0:
            print 'Can remove Column: ', x
    '''
    #this is where columns are dropped from each csv file
    for current in range(1,folds+1):
        dataframe = pd.read_csv('/home/skjena/data/testData'+'/fold_'+str(current)+'.csv')
        #dataframe = pd.read_csv(inputPath + '/ppmi_'+str(current)+'.csv')
        numCols = len(dataframe.columns) 
        for x in range(numCols-1,0,-1): 
            if Columns[x-1] == 0:
                dataframe = dataframe.drop(dataframe.columns[x], axis=1)
        dataframe.to_csv('/home/skjena/data/reducedData/fold_'+str(current)+'.csv', sep=',', header=False,float_format='%.2f', index=False)

ppmiReduction('/home/skjena/data/PPMI', 10)
