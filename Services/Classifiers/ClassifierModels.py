# -*- coding: utf-8 -*-
from sklearn.linear_model import LinearRegression, Ridge
from sklearn import svm
from SuperGLU.Classifiers.Metrics import calcR2
from SuperGLU.Classifiers.ModelFeature import FeatureSelector, ModelFeature

# Builder for Classifires
#------------------------------
class ClassifierBuilder(object):
    def __init__(self, modelMaker, features=None, params=None, modelParams=None):
        if features is None: features = []
        if params is None: params = {}
        if modelParams is None: modelParams = {}  
        self._modelMaker = modelMaker
        self._featureTypes = features
        self._params = params
        self._modelParams = modelParams

    def getFeatureTypes(self):
        return [x.getName() for x in self._featureTypes]

    def selectAllFeatures(self, inputs, outputs=None):
        allFeatures = []
        for featureType in self._featureTypes:
            features = self.selectFeatures(featureType, inputs, outputs)
            allFeatures.extend(features)
        features = sorted(features, key=lambda x: x.getName())
        return allFeatures

    def selectFeatures(self, featureType, inputs, outputs=None):
        if isinstance(featureType, FeatureSelector):
            features = featureType(inputs, outputs, self._params)
        elif isinstance(featureType, ModelFeature):
            features = [featureType]
        else:
            raise TypeError('Invalid feature selector or feature, got: %s'%(featureType,))
        return features

    def makeModel(self, features, inputs, outputs):
        featureVals = sorted([(f.getName(), f) for f in features])
        featureVals = [f for name, f in featureVals]
        model = self._modelMaker(featureVals, dict(self._modelParams))
        model.train(inputs, outputs)
        return model

    def calculateFeatureValues(self, inputs, outputs=None):
        features = self.selectAllFeatures(inputs, outputs)
        inputFeatureSets = []
        for inp in inputs:
            inpVals = [f(inp) for f in features]
            inputFeatureSets.append(inpVals)
        return inputFeatureSets

    def makeFeatureTable(self, inputs, outputs):
        features = self.selectAllFeatures(inputs, outputs)
        inputs = self.calculateFeatureValues(inputs, outputs)
        header = [f.getName() for f in features] + ['Output']
        outRecords = [header]
        for i, inp in enumerate(inputs):
            outRecord = inp + [outputs[i]]
            outRecords.append(outRecord)
        return outRecords

    def __call__(self, inputs, outputs):
        allFeatures = self.selectAllFeatures(inputs, outputs)
        model = self.makeModel(allFeatures, inputs, outputs)
        return model

# Stored Classifiers
#------------------------------
class ClassifierModel(object):
    def __init__(self, features, params=None):
        if params is None: params = {}
        self._params = dict(params)
        self._features = features

    def __call__(self, value):
        features = self.makeFeatures(value)
        return self._predict(features)

    def train(self, inputs, outputs):
        features = [self.makeFeatures(anInput) for anInput in inputs]
        self._train(features, outputs)

    def getFeatureNames(self):
        return [x.getName() for x in self._features]

    def getFeatureImportances(self):
        return [(name, '?') for name in self.getFeatureNames()]

    def makeFeatures(self, anInput):
        return [f(anInput) for f in self._features]

    def _predict(self, features):
        raise NotImplementedError

    def _train(self, features, outputs):
        pass

    def calcR2(self, inputs, outputs):
        vals = [self(anInput) for anInput in inputs]
        return calcR2(vals, outputs)

    def score(self, inputs, outputs):
        return self.calcR2(inputs, outputs)

class LinearClassModel(ClassifierModel):
    def __init__(self, features, params=None):
        if params is None: params = {}
        params = dict(params)
        self._valMin = params.pop('ValMin', None)
        self._valMax = params.pop('ValMax', None)
        super(LinearClassModel, self).__init__(features, params)
        self._model = None

    def getFeatureImportances(self):
        return [(name, self._model.coef_[i]) for i, name in enumerate(self.getFeatureNames())]
    
    def _train(self, features, outputs):
        #est = LinearRegression(**self._params)
        est = Ridge(**self._params)
        est.fit(features, outputs)
        self._model = est

    def _predict(self, features):
        val = float(self._model.predict([features]))
        if self._valMin  is not None:
            val = max(self._valMin, val)
        if self._valMax is not None:
            val = min(self._valMax, val)
        return val

class SVMModel(ClassifierModel):
    def __init__(self, features, params=None):
        super(SVMModel, self).__init__(features, params)
        self._model = None
        self._outputTransform = params.get('OutputTransform', lambda x: x)
    
    def _train(self, features, outputs):
        outputs = [self._outputTransform(o) for o in outputs]
        est = svm.SVC(kernel='linear', C=1.0, class_weight='auto')
        est.fit(features, outputs)
        self._model = est

    def _predict(self, features):
        return float(self._model.predict([features]))

