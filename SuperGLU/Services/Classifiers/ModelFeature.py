# -*- coding: utf-8 -*-
import operator
from SuperGLU.Util.Serialization import NamedSerializable

# Specific Features
class ModelFeature(NamedSerializable):
    def __init__(self, name):
        super(ModelFeature, self).__init__(None, name)

    def getName(self):
        return self._name

    def __eq__(self, other):
        return type(self) == type(other)

    def __ne__(self, other):
        return not (self.__eq__(other))
    
    def __call__(self, value):
        return NotImplementedError

class ReferenceDiffFeature(ModelFeature):
    def __init__(self, name, refVal, distance=None, transform=None):
        super(ReferenceDiffFeature, self).__init__(name)
        if distance is None: distance = operator.sub
        self._ref = refVal
        self._distance = distance
        self._transform = transform

    def __call__(self, value):
        if self._transform is not None:
            value = self._transform(value)
        return self._distance(value, self._ref)

    def __eq__(self, other):
        return (super(ReferenceDiffFeature, self).__eq__(other) and
                self._ref == other._ref and
                self._distance == other._distance and
                self._transform == other._transform)

class InSequenceFeature(ModelFeature):
    NAME_PREFIX = 'INSEQ_'
    def __init__(self, name, target):
        super(InSequenceFeature, self).__init__(name)
        self._target = target

    def __eq__(self, other):
        return (super(InSequenceFeature, self).__eq__(other) and
                self._target == other._target)
        
    def __call__(self, value):
        return int(self._target in value)

class OrderFeature(ModelFeature):
    NAME_PREFIX = 'ORDERING_'
    def __init__(self, name, ordering):
        super(OrderFeature, self).__init__(name)
        self._ordering = ordering

    def __eq__(self, other):
        return (super(OrderFeature, self).__eq__(other) and
                self._ordering == other._ordering)

    def __call__(self, value):
        for w in self._ordering:
            try:
                newIndex = value.index(w)
            except ValueError:
                newIndex = -1
            if newIndex >= 0:
                value = value[newIndex:]
            else:
                return 0
        return 1


class CountSubseqFeature(OrderFeature):
    NAME_PREFIX = 'COUNT_SUBSEQ_'
    def __init__(self, name, ordering, window=None):
        if window is None: window = len(ordering)
        super(CountSubseqFeature, self).__init__(name, ordering)
        self._window = window
        if self._window is not None and len(ordering) > self._window:
            raise ValueError("Ordering longer than window size (%i) for: %s"%(window, ordering))

    def __eq__(self, other):
        return (super(CountSubseqFeature, self).__eq__(other) and
                self._window == other._window)

    def __call__(self, value):
        valueChecker = super(CountSubseqFeature, self).__call__
        if len(value) <= len(self._ordering):
            return valueChecker(value)
        else:
            indices = set()
            for i in xrange(1+len(value)-self._window):
                windowSeq = value[i:i+self._window]
                #print windowSeq, valueChecker(windowSeq)
                if valueChecker(windowSeq):
                    position = windowSeq.index(self._ordering[0])
                    indices.add(i+position)
            #print indices
            return len(indices)
            
    
class MappingFeature(ModelFeature):
    def __init__(self, name, aDict, default=0):
        super(MappingFeature, self).__init__(name)
        self._dict = aDict
        self._default = default

    def __eq__(self, other):
        return (super(MappingFeature, self).__eq__(other) and
                self._dict == other._dict and
                self._default == other._default)

    def __call__(self, value):
        return self._dict.get(value, self._default)

class GetItemFeature(ModelFeature):
    def __init__(self, name, key, default=None, allowDefault=False):
        super(GetItemFeature, self).__init__(name)
        self._key = key
        self._default = default
        self._allowDefault = allowDefault

    def __eq__(self, other):
        return (super(GetItemFeature, self).__eq__(other) and
                self._key == other._key and
                self._default == other._default and
                self._allowDefault == other._allowDefault)

    def __call__(self, value):
        if self._allowDefault:
            return value.get(self._key, self._default)
        else:
            return value[self._key]

class MethodCallFeature(ModelFeature):
    def __init__(self, name, functName, args=None, kwds=None,
                 default=None, allowDefault=False):
        if args is None: args = []
        if kwds is None: kwds = {}
        super(MethodCallFeature, self).__init__(name)
        self._functName = functName
        self._args = args
        self._kwds = kwds
        self._default = default
        self._allowDefault = allowDefault

    def __eq__(self, other):
        return (super(MethodCallFeature, self).__eq__(other) and
                self._functName == other._functName and
                self._args == other._args and
                self._kwds == other._kwds and
                self._default == other._default and
                self._allowDefault == other._allowDefault)

    def __call__(self, value):
        if self._allowDefault and self._functName not in getattr(value):
            return self._default
        else:
            return getattr(value, self._functName)(*self._args, **self._kwds)

class TransformedFeature(ModelFeature):
    def __init__(self, name, features):
        super(TransformedFeature, self).__init__(name)
        self._features = tuple(features)

    def __eq__(self, other):
        return (super(TransformedFeature, self).__eq__(other) and
                self._features == other._features)

    def __call__(self, value):
        for f in self._features:
            value = f(value)
        return value

# Feature Generators
class FeatureSelector(NamedSerializable):
    def __init__(self, name):
        if len(name) == 0 or '_' in name:
            raise ValueError("Feature type names but be non-empty and cannot have an '_' symbol")
        super(FeatureSelector, self).__init__(None, name)

    def binByOutput(self, inputs, outputs):
        classMap = dict([(o, []) for o in outputs])
        for i, val in enumerate(inputs):
            out = outputs[i]
            classMap[out].append(val)
        return classMap
    
    def __call__(self, inputs, outputs, params=None):
        return []

if __name__ == '__main__':
    x = CountSubseqFeature('aCount', [1,2,3], 5)
    print x([1])
    print x([1,2,3])
    print x(range(10))
    print x(range(4)*5)
    print x([1,1,2,2,3,3]*2)
    
