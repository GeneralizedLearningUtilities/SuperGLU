# -*- coding: utf-8 -*-
import math
import numpy
from sklearn import metrics

def calcR2(predictions, outputs):
    if False:
        return numpy.corrcoef([predictions], [outputs])[0, 1]
    else:
        meanOutput = float(sum(outputs))/len(outputs)
        totalSquares = sum([(out - meanOutput)**2.0 for out in outputs])
        residualSquares = sum([(out - predictions[i])**2.0 for i, out in enumerate(outputs)])
        if totalSquares == 0:
            rSquared = 0.0
        else:
            rSquared = 1.0 - float(residualSquares)/totalSquares
        return rSquared

def calcMatthewsCorr(predicted, actual, labels=None):
    if labels is None: labels = [-1, 1]
    confMatrix = metrics.confusion_matrix(actual, predicted, labels)
    tp = float(confMatrix[0][0])
    tn = float(confMatrix[1][1])
    fp = float(confMatrix[0][1])
    fn = float(confMatrix[1][0])
    bottom = math.sqrt((tp + fp)*(tp + fn)*(tn + fp)*(tn + fn))
    if bottom == 0:
        print "Warning: Confusion matrix was incomplete"
        return -0
    else:
        return (tp*tn - fp*fn)/bottom
