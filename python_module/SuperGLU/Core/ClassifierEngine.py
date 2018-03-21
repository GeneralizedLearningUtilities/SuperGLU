# -*- coding: utf-8 -*-
import datetime
import re
from urllib.parse import urlparse
from SuperGLU.Util.Serialization import SuperGlu_Serializable

class ClassifierEngine(SuperGlu_Serializable):
    """
    An engine for calculating the full set of classifications
    based on a starting set of classifications of interest.
    """

    def __init__(self, classifiers=None, resolver=None):
        """
        Initialize the classification engine
        This engine takes classifiers, which must be able to
        infer membership based on properties (directly or indirectly)
        and a resolver, which uses global constraints over groups that
        enforce relationships like mutual exclusivity or priority.
        @param classifiers: A list of class specifications
        @type classifiers: list of ClassifierSpecification
        @param resolver: A global function that imposes global priority or exclusivity (XOR) conditions
        @type resolver: callable
        """
        if classifiers is None: classifiers = []
        self._classifiers = dict([(c.getName(), c) for c in classifiers])
        self._resolver = resolver
        self._instance = None
        self._trueSet = set()
        self._evaluatedSet = set()
        self._validateConditions()

    def _validateConditions(self):
        """
        Validate that the conditions between class specifiers are
        acyclic, so that termination is guarranteed to end properly.
        """
        classes = {}
        # Get Direct Classes Dependencies
        for name, c in list(self._classifiers.items()):
            classes[name] = set([c2.getClasses() for c2 in c.getConditions()])
        for x, xDeps in classes:
            for y in xDeps:
                if x in classes[y]:
                    raise KeyError("Cyclic dependency between: <%s> an <%s>"%(x, y))

    def reset(self):
        """ Reset the list of evaluated and true items """

    def getClassMemberships(self, instance, classes=None):
        """
        Get the classes that the instance belongs to, out of the given
        set of classes (or all known classes, if not constrained set given
        @param instance: The instance to classify
        @type instance: object
        @param classes: A list of class specifications to check.  If None, check all.
        @type classes: list of ClassifierSpecification
        """
        if classes is None: classes = list(self._classifiers.keys())
        for className in classes:
            if className not in self._evaluatedSet:
                if self._classifiers[className].isMember(instance, self):
                    self._trueSet.add(className)
                self._evaluatedSet.add(className)
        return list(classes & self._trueSet)


class ClassifierSpecification(SuperGlu_Serializable):
    """
    A classifier that contains the requirements for a single
    classification.  However, the requirements for this
    classifier may depend on the values of other classifiers
    (e.g., for mutually-exclusive classifications)
    """

    def __init__(self, name, necessary=None, exclusions=None, sufficiencies=None):
        """
        @param name: Name for the specification
        @type name: str
        @param necessary: Necessary conditions.  These should be quick to evaluate, to discard irrelevant items.
        @type necessary: list of ClassifierCondition
        @param exclusions: Conditions that, if true, exclude an object from membership (i.e., !necessary)
        @type exclusions: list of ClassifierCondition
        @param sufficiencies: If necessary and exclusions pass, and any of thes are true, object is a member.
        @type sufficiencies: ClassifierCondition
        """
        super(ClassifierSpecification, self).__init__()
        if necessary is None: necessary = tuple()
        if exclusions is None: exclusions = tuple()
        if sufficiencies is None: sufficiencies = tuple()
        self._name = name
        self._necessary = tuple(necessary)
        self._exclusions = tuple(exclusions)
        self._sufficiencies = tuple(sufficiencies)

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._name == other._name and
                self._necessary == other._necessary and
                self._exclusions == other._exclusions and
                self._sufficiencies == other._sufficiencies)

    def getName(self):
        """ Get the name of the classifier """
        return self._name

    def isMember(self, instance, engine=None):
        """
        Check if an instance is a member of this class
        @param instance: Object to check for membership
        @type instance: object
        @param engine: Optionally, an engine to run this classifier
        @type engine: ClassifierEngine
        @return: True if instance is a member of this class.  False if False or undecidable.
        @rtype: bool
        """
        for need in self._necessary:
            if not need(instance, engine):
                return False
        for exclude in self._exclusions:
            if exclude(instance, engine):
                return False
        for sufficient in self._sufficiencies:
            if sufficient(instance, engine):
                return True
        return False

    def getConditions(self):
        """ Get the full list of all conditions used by this specification """
        return list(self._necessary + self._exclusions + self._sufficiencies)

#--------------------------------
# Classifier Conditions
#--------------------------------
class ClassifierCondition(SuperGlu_Serializable):
    """ A condition for a classifier that evaluates to True/False"""

    def __eq__(self, other):
        return type(self) == type(other)

    def __call__(self, instance, engine=None):
        """
        Check if a condition holds for this instance
        @param instance: An object to check
        @type instance: object
        @param engine: A classification engine, for tracking membership
        @type engine: ClassificationEngine
        @return: True if condition holds, False if it does not
        @rtype: bool
        """
        raise NotImplementedError

    def getClasses(self):
        """
        List all the classification specifications this depends on
        @return: List of specifications
        @rtype: list of ClassificationSpecification
        """
        return []


class AtomicClassifierCondition(ClassifierCondition):
    """
    A classifier that checks for a specific relationship or
    property for a class.
    """

    def __init__(self, propName=None):
        super(AtomicClassifierCondition, self).__init__()
        self._propName = propName

    def __eq__(self, other):
        return (super(AtomicClassifierCondition, self).__eq__(other) and
                self._propName == other._propName)

class DataClassifierCondition(AtomicClassifierCondition):
    """ A classification that only depends on data values """
    pass


class ObjectClassifierCondition(AtomicClassifierCondition):
    """ A classification that depends on membership in other classes """

    def __init__(self, propName=None, classes=None):
        super(ObjectClassifierCondition, self).__init__(propName)
        if classes is None: classes = tuple()
        self._classes = tuple(classes)

    def getClasses(self):
        return list(self._classes)

    def __eq__(self, other):
        return (super(ObjectClassifierCondition, self).__eq__(other) and
                self._propName == other._propName and
                set(self._classes) == set(other._classes))


class CompositeClassifierCondition(ClassifierCondition):
    """ A condition that combines other conditions """

    def __init__(self, conditions):
        super(CompositeClassifierCondition, self).__init__()
        self._conditions = tuple(conditions)

    def getClasses(self):
        """ Get all the class names involved """
        return list(set([c for x in self._conditions for c in x.getClasses()]))

    def __eq__(self, other):
        return (super(CompositeClassifierCondition, self).__eq__(other) and
                self._conditions == other._conditions)

#--------------------------------
# Data Property Conditions
#--------------------------------

class InEnumeratedCondition(DataClassifierCondition):
    """ Check if an element is a member of a given set """

    def __init__(self, propName=None, elements=None):
        super(InEnumeratedCondition, self).__init__(propName)
        if elements is None: elements = set()
        self._elements = set(elements)

    def __call__(self, instance, engine=None):
        return instance in self._elements


class NumericClassifierCondition(DataClassifierCondition):
    """ A classifier condition that checks if data is numeric """

    def __call__(self, instance, engine=None):
        return isinstance(instance, (int, float))


class NumericRangeCondition(NumericClassifierCondition):
    """ Check if a number is in a particular range """

    def __init__(self, propName=None, minVal=None, maxVal=None):
        super(NumericRangeCondition, self).__init__(propName)
        self._minVal = minVal
        self._maxVal = maxVal
        self.validate()

    def validate(self):
        if self._minVal is None and self._maxVal is None:
            raise ValueError("Classifier range must have one non-None boundary")
        if self._minVal is not None and not isinstance(self._minVal, (int, float)):
            raise TypeError("Minimum value was not a number.  Got: %s"%(self._minVal))
        if self._maxVal is not None and not isinstance(self._maxVal, (int, float)):
            raise TypeError("Maximum value was not a number.  Got: %s"%(self._maxVal))
        if (self._minVal is not None and self._maxVal is not None and self._minVal >= self._maxVal):
            raise ValueError("Maximum value was lower than minumum.  Got: (%s, %s)"%(self._minVal, self._maxVal))

    def __call__(self, instance, engine=None):
        if not super(NumericRangeCondition, self).__call__(instance):
            return False
        elif self._minVal is not None and instance < self._minVal:
            return False
        elif self._maxVal is not None and instance > self._maxVal:
            return False
        return True

    def __eq__(self, other):
        return (super(NumericRangeCondition, self).__eq__(other) and
                self._minVal == other._minVal and
                self._maxVal == other._maxVal)


class SequenceClassifierCondition(DataClassifierCondition):
    """ A classifier condition that requires an iterable instance """

    def __call__(self, instance, engine=None):
        return hasattr(instance, '__iter__')


class SequenceElementsCondition(SequenceClassifierCondition):
    """ A condition that checks each element """

    def __init__(self, propName=None, conditions=None):
        super(SequenceElementsCondition, self).__init__(propName)
        if conditions is None: conditions = tuple()
        self._conditions = tuple(conditions)

    def __call__(self, instance, engine=None):
        if not super(SequenceElementsCondition, self).__call__(instance):
            return False
        for x in instance:
            for condition in self._conditions:
                # Engine not passed in, as these are different instances
                if not condition(x):
                    return False
        return True

# Sequence Length check

class SequenceLengthCondition(SequenceClassifierCondition):
    """Check if the length of instance is in a particular range"""

    def __init__(self, propName=None, minLen=None, maxLen=None):
        super(SequenceLengthCondition, self).__init__(propName)
        self._minLen = minLen
        self._maxLen = maxLen

    def __call__(self, instance, engine=None):
        if not super(SequenceLengthCondition, self).__call__(instance):
            return False
        elif self._minLen is not None and len(instance) < self._minLen:
            return False
        elif self._maxLen is not None and len(instance) > self._maxLen:
            return False
        else:
            return True

class SetIntersectionCondition(SequenceClassifierCondition):
    """Check if intersection of elements and """

    def __init__(self, propName=None, elements=None, type=None):
        super(SetIntersectionCondition, self).__init__(propName)
        self._elements = set(elements)
        self._type = type

    def __call__(self, instance, engine=None):
        if not super(SetIntersectionCondition, self).__call__(instance):
            return False

        instanceSet = set(instance)

        if type == 'NON_ZERO':
            if instanceSet.intersection(self._elements) == set([]):
                return False
            else:
                return True

        if type == 'SAME':
            if instanceSet == self._elements:
                return True
            else:
                return False

        if type == 'SUBSET':
            if instanceSet <= self._elements:
                return True
            else:
                return False

        if type == 'SUPERSET':
            if instanceSet >= self._elements:
                return True
            else:
                return False

class ExistsInSetCondition(SequenceClassifierCondition):
    """given a list of elements, at least one must satisfy the condition"""

    def __init__(self, propName=None, condition=None):
        super(ExistsInSetCondition, self).__init__(propName)
        self._condition = condition

    def __call__(self, instance, engine=None):
        if not super(ExistsInSetCondition, self).__call__(instance):
            return False

        for x in instance:
            if self._condition(x):
                return True

        return False

class AllInSetCondition(SequenceClassifierCondition):
    """given a list of elements, all must satisfy the condition"""

    def __init__(self, propName=None, condition=None):
        super(AllInSetCondition, self).__init__(propName)
        self._condition = condition

    def __call__(self, instance, engine=None):
        if not super(AllInSetCondition, self).__call__(instance):
            return False

        for x in instance:
            if not self._condition(x):
                return False

        return True

class NoneInSetCondition(SequenceClassifierCondition):
    """given a list of elements, none should satisfy the condition"""

    def __init__(self, propName=None, condition=None):
        super(AllInSetCondition, self).__init__(propName)
        self._condition = condition

    def __call__(self, instance, engine=None):
        if not super(NoneInSetCondition, self).__call__(instance):
            return False

        for x in instance:
            if self._condition(x):
                return False

        return True

class ListIntersectionCondition(SequenceClassifierCondition):
    """just compare if lists are the same"""

    def __init__(self, propName=None, elements=None):
        super(ListIntersectionCondition, self).__init__(propName)
        self._elements = elements

    def __call__(self, instance, engine=None):
        if not super(ListIntersectionCondition, self).__call__(instance):
            return False

        if self._elements == instance:
            return True

        return False

# Sequence matching
# - set equivalences: Non-zero intersection, same elements, all elements part of comparison set
# - ordered set equivalent: Same elements in same order
# - Validate element at index

# String matching (subclass of sequence elements matching)
# - RegEx
# - Is Valid URL?
class StringCondition(SequenceClassifierCondition):
    """String matches condition"""

    def __init__(self, propName=None):
        super(StringCondition, self).__init__(propName)

    def __call__(self, instance, engine=None):
        if not super(StringCondition, self).__call__(instance):
            return False
        return isinstance(instance, str)

class RegExCondition(StringCondition):
    """Checking if the string matches a regex pattern"""

    def __init__(self, propName=None, regex=None):
        super(RegExCondition, self).__init__(propName)
        self._regex = regex
        self._pattern = re.compile(r'\b'+regex+r'\b')

    def __call__(self, instance, engine=None):
        if not super(RegExCondition, self).__call__(instance):
            return False
        return self._pattern.search(instance) is not None

class IsValidURLCondition(StringCondition):
    """Check if the string is an valid URL"""

    def __ini__(self, propName, URL=None, strict=True):
        super(IsValidURLCondition, self).__init__(propName)
        self._url = URL
        self._strict = strict

    def __call__(self, instance, engine=None):
        if not super(IsValidURLCondition, self).__call__(instance):
            return False

        ul = urlparse(self._url)

        if self._strict:
            try:
                assert all([ul.scheme, ul.netloc])
                assert ul.scheme in ['http', 'https', 'ftp']
                return True
            except AssertionError:
                return False
        else:
##########To be determined####################################
            return True


# Map Matching (check if has __contains__, in addition to __iter__):
# - Validate the keys
# - Validate the values
# - Validate key-value pairs
# - Validate a value with a specific key

class MapClassifierCondition(SequenceClassifierCondition):
    """Map Matching"""

    def __init__(self, propName=None):
        super(MapClassifierCondition, self).__init__(propName)

    def __call__(self, instance, engine=None):
        if not super(MapClassifierCondition, self).__call__(instance):
            return False
        return hasattr(instance, '__contains__')

class MapKeysCondition(MapClassifierCondition):
    """Validate the keys"""

    def __init__(self, propName=None, conditions=None):
        super(MapKeysCondition, self).__init__(propName)
        if conditions is None:
            conditions = tuple()
        self._conditions = tuple(conditions)

    def __call__(self, instance, engine=None):
        if not super(MapKeysCondition, self).__call__(instance):
            return False
        for x in list(instance.keys()):
            for condition in self._conditions:
                if not condition(x):
                    return False
        return True

class MapValuesCondition(MapClassifierCondition):
    """Validate the values"""

    def __init__(self, propName=None, conditions=None):
        super(MapValuesCondition, self).__init__(propName)
        if conditions is None:
            conditions = tuple()
        self._conditions = tuple(conditions)

    def __call__(self, instance, engine=None):
        if not super(MapValuesCondition, self).__call__(instance):
            return False
        for x in list(instance.values()):
            for condition in self._conditions:
                if not condition(x):
                    return False
        return True



class MapKeysIntersectionCondition(MapClassifierCondition):
    """Check the relationships between sets"""

    def __init__(self, propName=None, elements=None, aType=None):
        super(MapKeysIntersectionCondition, self).__init__(propName)
        self._elements = set(elements)
        self._type = aType

    def __call__(self, instance, engine=None):
        if not super(MapKeysIntersectionCondition, self).__call__(instance):
            return False

        keyset = set(instance.keys())

        if self._type == 'NON_ZERO':
            if len(keyset.intersection(self._elements)) > 0:
                return False
            else:
                return True

        elif self._type == 'SAME':
            if keyset == self._elements:
                return True
            else:
                return False

        elif self._type == 'SUBSET':
            if keyset <= self._elements:
                return True
            else:
                return False

        elif self._type == 'SUPERSET':
            if keyset >= self._elements:
                return True
            else:
                return False
        else:
            raise TypeError("Invalid Intersection Type for Condition: %s"%(type,))

class MapValuesIntersectionCondition(MapClassifierCondition):
    """Check the relationships between sets"""

    def __init__(self, propName=None, elements=None, type=None):
        super(MapKeysIntersectionCondition, self).__init__(propName)
        self._elements = set(elements)
        self._type = type

    def __call__(self, instance, engine=None):
        if not super(MapKeysIntersectionCondition, self).__call__(instance):
            return False

        valueset = set(instance.values())

        if type == 'NON_ZERO':
            if valueset.intersection(self._elements) == set([]):
                return False
            else:
                return True

        if type == 'SAME':
            if valueset == self._elements:
                return True
            else:
                return False

        if type == 'SUBSET':
            if valueset <= self._elements:
                return True
            else:
                return False

        if type == 'SUPERSET':
            if valueset >= self._elements:
                return True
            else:
                return False

class MapItemsCondition(MapClassifierCondition):
    """Validate every items"""

    def __init__(self, propName=None, conditions=None):
        super(MapItemsCondition, self).__init__(propName)
        if conditions is None: conditions = tuple()
        self._conditions = tuple(conditions)

    def __call__(self, instance, engine=None):
        if not super(MapItemsCondition, self).__call__(instance):
            return False
        for x in instance:
            for condition in self._conditions:
                if not condition(x):
                    return False

        return True


class MapElementCondition(MapClassifierCondition):
    """Validate every elements"""

    def __init__(self, propName=None, conditions=None):
        super(MapItemsCondition, self).__init__(propName)
        if conditions is None: conditions = tuple()
        self._conditions = tuple(conditions)

    def __call__(self, instance, engine=None):
        if not super(MapItemsCondition, self).__call__(instance):
            return False
        for x in list(instance.values()):
            for condition in self._conditions:
                if not condition(x):
                    return False

        return True




#-----------------------------------------
# ISO Standard Dates
# - Validate that date falls in a range
#-----------------------------------------
class DateClassifierCondition(DataClassifierCondition):
    """ISO Standard Dates"""


    def __call__(self, instance, engine=None):
        return isinstance(instance, datetime.date)

class DateRangeCondition(DateClassifierCondition):
    """Validate that date falls in a range"""

    def __init__(self, propName=None, minDate=None, maxDate=None):
        super(DateRangeCondition, self).__init__(propName)
        self._minDate = minDate
        self._maxDate = maxDate

    def validate(self):
        if self._minDate is None and self._maxDate is None:
            raise ValueError("Classifier range must have one non-None boundary")
        if self._minDate is not None and not isinstance(self._minDate, datetime.date):
            raise ValueError("Min date was not a datetime.date. Got %s"%s(self._minDate))
        if self._maxDate is not None and not isinstance(self._maxDate, datetime.date):
            raise ValueError("Max date was not a datetime.date. Got %s"%s(self._maxDate))


    def __call__(self, instance, engine=None):
        if not super(DateRangeCondition, self).__call__(instance):
            return False
        elif self._minDate is not None and instance < self._minDate:
            return False
        elif self._maxDate is not None and instance > self._maxDate:
            return False
        return True


#--------------------------------
# Object Property Conditions
#--------------------------------
class IsMemberClassifierCondition(ObjectClassifierCondition):
    """ A classification that checks for membership in another class """

    def __init__(self, aClass):
        propName = "IsMember"
        super(ObjectClassifierCondition, self).__init__(propName, [aClass])

    def __call__(self, instance, engine=None):
        return len(engine.getClassMemberships(instance, self._classes)) > 0

#-------------------------
# Composite Conditions
#-------------------------
class NOTCondition(CompositeClassifierCondition):

    def __init__(self, condition):
        super(NOTCondition, self).__init__([conditions])

    def __call__(self, instance, engine=None):
        return not self._conditions[0](instance, engine)

class ANDCondition(CompositeClassifierCondition):

    def __call__(self, instance, engine=None):
        return all(x(instance, engine) for x in self._conditions)

class ORCondition(CompositeClassifierCondition):

    def __call__(self, instance, engine=None):
        return any(x(instance, engine) for x in self._conditions)

class XORCondition(CompositeClassifierCondition):

    def __call__(self, instance, engine=None):
        ret = False
        for x in self._conditions:
            ret^= x(instance, engine)
        return ret
