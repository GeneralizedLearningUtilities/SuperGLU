# -*- coding: utf-8 -*-
from sklearn.linear_model import LinearRegression, Ridge
from sklearn import svm
from SuperGLU.Classifiers.Metrics import calcR2
from SuperGLU.Classifiers.ModelFeature import FeatureSelector, ModelFeature

# Builder for Classifires
#------------------------------
class ClassifierBuilder(object):
    """
    Class for building a classifier from data, which creates both the feature set and
    the trained classifier from the available data.
    """
    def __init__(self, modelMaker, features=None, params=None, modelParams=None):
        """
        Initialize the Classifier Builder
        @param modelMaker: A callable class that creates a trainable model with
                           certain features and expected model params
        @param featureTypes: A list of categories for of feature that could be created, where one
                             feature type might make many features (e.g., "every n-tuple of words that occurs")
        @param params: Parameters for evaluating feature types
        @param modelParams: Parameters to pass in to the model maker (e.g., update rates, convergence criteria)
        """
        if features is None: features = []
        if params is None: params = {}
        if modelParams is None: modelParams = {}  
        self._modelMaker = modelMaker
        self._featureTypes = features
        self._params = params
        self._modelParams = modelParams

    # ------------------------------------------------
    # Functions to Generate a Set of Possible Features
    # ------------------------------------------------
    def getFeatureTypes(self):
        """ The names of the types of features to create """
        return [x.getName() for x in self._featureTypes]

    def selectAllFeatures(self, inputs, outputs=None):
        """ Identify the set of possible features across all feature types """
        allFeatures = []
        for featureType in self._featureTypes:
            features = self.selectFeatures(featureType, inputs, outputs)
            allFeatures.extend(features)
        features = sorted(features, key=lambda x: x.getName())
        return allFeatures

    def selectFeatures(self, featureType, inputs, outputs=None):
        """ Identify the set of possible features for a given feature type """
        if isinstance(featureType, FeatureSelector):
            features = featureType(inputs, outputs, self._params)
        elif isinstance(featureType, ModelFeature):
            features = [featureType]
        else:
            raise TypeError('Invalid feature selector or feature, got: %s'%(featureType,))
        return features

    # -------------------------------------------------
    # Functions to Calculate a Matrix of Feature Values
    # -------------------------------------------------
    def calculateFeatureValues(self, inputs, outputs=None):
        """ Calculate the matrix of feature values to use for training """
        features = self.selectAllFeatures(inputs, outputs)
        inputFeatureSets = []
        for inp in inputs:
            inpVals = [f(inp) for f in features]
            inputFeatureSets.append(inpVals)
        return inputFeatureSets

    def makeFeatureTable(self, inputs, outputs):
        """ Create a table of features, where the outputs are added as a final column """
        features = self.selectAllFeatures(inputs, outputs)
        inputs = self.calculateFeatureValues(inputs, outputs)
        header = [f.getName() for f in features] + ['Output']
        outRecords = [header]
        for i, inp in enumerate(inputs):
            outRecord = inp + [outputs[i]]
            outRecords.append(outRecord)
        return outRecords

    # -------------------------------------------------
    # Functions to Train Models based on Data
    # -------------------------------------------------
    def makeModel(self, features, inputs, outputs):
        """ Create a trained model from the given features, inputs, and outputs """
        featureVals = sorted([(f.getName(), f) for f in features])
        featureVals = [f for name, f in featureVals]
        model = self._modelMaker(featureVals, dict(self._modelParams))
        model.train(inputs, outputs)
        return model

    def __call__(self, inputs, outputs):
        """ Run the Classifier Builder on data, selecting features and training a model with them """
        allFeatures = self.selectAllFeatures(inputs, outputs)
        model = self.makeModel(allFeatures, inputs, outputs)
        return model

# Stored Classifiers
#------------------------------
class ClassifierModel(object):
    """ Wrapper/base class for models that are trained based on some features """
    
    def __init__(self, features, params=None):
        """
        Initialize the model
        @param features: The set of features to calculate, based on some input data
        @param params: Parameters needed to train the model
        """
        if params is None: params = {}
        self._params = dict(params)
        self._features = features

    def __call__(self, value):
        """
        Turn an instance into features, then predict the output
        @param value: Any valid object that the features can process
        @return: Predicted output label
        """
        features = self.makeFeatures(value)
        return self._predict(features)

    def train(self, inputs, outputs):
        """
        Train a classifier model
        @param inputs: Input instances
        @param outputs: Output labels
        """
        features = [self.makeFeatures(anInput) for anInput in inputs]
        self._train(features, outputs)

    def getFeatureNames(self):
        """ Return the names of all features """
        return [x.getName() for x in self._features]

    def getFeatureImportances(self):
        """ Return the relative importance weights of all features, if available """
        return [(name, '?') for name in self.getFeatureNames()]

    def makeFeatures(self, anInput):
        """ Turn an instance input into a vector of features """
        return [f(anInput) for f in self._features]

    def _predict(self, features):
        """ Predict an output label based on feature values """
        raise NotImplementedError

    def _train(self, features, outputs):
        """ Train some classifier model """
        pass

    def calcR2(self, inputs, outputs):
        """ Calculate a basic R2 value for the given input-output set """
        vals = [self(anInput) for anInput in inputs]
        return calcR2(vals, outputs)

    def score(self, inputs, outputs):
        """ Calculate a score for this model's predictions based on the input-output set """
        return self.calcR2(inputs, outputs)


class LinearClassModel(ClassifierModel):
    """ Wrapper for a linear classifier model """
    
    def __init__(self, features, params=None):
        """
        Initialize the classifier
        @param valMin: A minimum value to apply to the output (floor)
        @param valMax: A maximum value to apply to the output (ceiling)
        """
        if params is None: params = {}
        params = dict(params)
        self._valMin = params.pop('ValMin', None)
        self._valMax = params.pop('ValMax', None)
        super(LinearClassModel, self).__init__(features, params)
        self._model = None

    def getFeatureImportances(self):
        """ Return feature importances, which are the coefficients """
        return [(name, self._model.coef_[i]) for i, name in enumerate(self.getFeatureNames())]
    
    def _train(self, features, outputs):
        """ Fit a linear regression model """
        #est = LinearRegression(**self._params)
        est = Ridge(**self._params)
        est.fit(features, outputs)
        self._model = est

    def _predict(self, features):
        """ Predict labels for the feature vector, applying the min-max as bounds """
        val = float(self._model.predict([features]))
        if self._valMin  is not None:
            val = max(self._valMin, val)
        if self._valMax is not None:
            val = min(self._valMax, val)
        return val


class SVMModel(ClassifierModel):
    """ Wrapper for an SVM model """
    DEFAULT_KERNEL = 'linear'
    DEFAULT_C = 1.0
    DEFAULT_WEIGHT = 'auto'
    
    def __init__(self, features, params=None):
        """
        Initialize the SVM Model wrapper
        @param OutputTransform: A transform function to the apply to the SVM model output (e.g., binning)
        """
        self._outputTransform = params.pop('OutputTransform', lambda x: x)
        super(SVMModel, self).__init__(features, params)
        self._model = None
        self._loadDefaultParams(False)

    def _loadDefaultParams(self, overwrite=False):
        params = {'kernel' : self.DEFAULT_KERNEL,
                  'C' : self.DEFAULT_C,
                  'class_weight' : 'auto'}
        for k, v in params.items():
            if overwrite or k not in self._params:
                self._params[k] = v
    
    def _train(self, features, outputs):
        """ Train an SVM model, transforming the features first """
        outputs = [self._outputTransform(o) for o in outputs]
        est = svm.SVC(kernel='linear', C=1.0, class_weight='auto')
        est.fit(features, outputs)
        self._model = est

    def _predict(self, features):
        """ Predict a value using the SVM model """
        return float(self._model.predict([features]))

