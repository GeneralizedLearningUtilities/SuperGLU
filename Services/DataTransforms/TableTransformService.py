"""
This service converts one table into another table,
by changing the headings (e.g., add, remove, re-sort),
and possibly adding calculated fields to the table.
"""
from SuperGLU.Util.Serialization import NamedSerializable
from SuperGLU.Core.MessagingGateway import BaseService

class TableTransformService(BaseService):
    def __init__(self, functions=None, anId=None, gateway=None, authenticator=None):
        """
        Receive a list of TableTransform instances,
        These will be turned into a map of the function name to
        the instance, so that these can be used to evaluate data.
        """
        if functions is None: functions = []
        super(TableTransformService, self).__init__(anId, gateway, authenticator)
        self._functions = dict([(x.getName(), x) for x in functions])
        if IdentityTransform.DEFAULT_NAME not in self._functions:
            self._functions[IdentityTransform.DEFAULT_NAME] = IdentityTransform()

    def getFunction(self, name):
        return self._functions[name]

    def transform(self, table, outputFields=None, **kwds):
        # Properly format output fields
        if outputFields is None: outputFields = []
        # Early return: No transforms, other than adding header
        if len(table) == 0 or outputFields is None:
            return [[name for name, functs in outputFields]]
        # Take name-only fields and turn them into null functions
        for i, f in enumerate(outputFields):
            if isinstance(f, basestring):
                outputFields[i] = (f, None)
        # If no function declared, assume an identity with col of same name
        for i, (name, data) in enumerate(outputFields):
            if data is None:
                outputFields[i] = (name, (IdentityTransform.DEFAULT_NAME,
                                          {IdentityTransform.FIELD_NAME : name}))
            elif data[1] is None:
                outputFields[i] = (name, (data[0], {}))
        header = table[0]
        newTable = [[name for name, funct in outputFields]] + [[] for x in xrange(len(table)-1)]
        for name, data in outputFields:
            functName, params = data
            # Add default extra params
            for kwdX, kwdVal in kwds:
                if kwdX not in params:
                    params[kwdX] = kwdVal
            function = self.getFunction(functName)
            for i, row in enumerate(table[1:]):
                rowData = dict([(header[anIndex], dat) for anIndex, dat in enumerate(row)])
                processedVal = function(rowData, i, header, table, **params)
                newTable[i+1].append(processedVal)
        return newTable


class TableTransform(NamedSerializable):
    DEFAULT_NAME = None
    def __init__(self, id=None, name=None):
        if name is None: name = self.DEFAULT_NAME
        super(TableTransform, self).__init__(id, name)

    def __call__(self, rowDict, rowNum, header, matrix, **kwds):
        raise NotImplementedError

    
class IdentityTransform(TableTransform):
    """
    Identity tranform.  Expects param kwds to include:
    @param FIELD_NAME: Name of the existing field to pull the value from
    @type FIELD_NAME: str
    """
    DEFAULT_NAME = 'Identity'
    FIELD_NAME = 'fieldName'

    def __call__(self, rowDict, rowNum, header, matrix, **kwds):
        name = kwds[self.FIELD_NAME]
        return rowDict.get(name, None)

class AverageFieldsTransform(TableTransform):
    """
    Average over tranform.  Expects param kwds to include:
    @param FIELD_NAMES: List of fields
    @type FIELD_NAMES: list of str
    """
    DEFAULT_NAME = 'Average'
    FIELD_NAMES = 'fieldNames'

    def __call__(self, rowDict, rowNum, header, matrix, **kwds):
        fieldNames = kwds[self.FIELD_NAMES]
        vals = [rowDict[x] for x in fieldNames if x in rowDict]
        if len(vals) > 0:
            return sum(vals)/float(len(vals))
        else:
            return None

if __name__ == '__main__':
    # Setup
    averager = AverageFieldsTransform()
    functions = [averager]
    transformer = TableTransformService(functions)

    # Make some sample data
    myData = [['A', 'B', 'C', 'D']]
    for i in xrange(3):
        if i%2 == 0:
            myData.append(range(0,4,1))
        else:
            myData.append(range(3,-1,-1))
    print "Original"
    print myData
    print

    # Re-arrange Columns
    sortColsFunct = ['B', 'C', 'D', 'A']
    myData = transformer.transform(myData, sortColsFunct)
    print "Rearranged"
    print myData
    print

    # Add identity columns that duplicate rows B and D
    outfieldIdentities = ['A', 'B', 'C', 'D',
                          ('B2', ('Identity', {'fieldName':'B'}))]
    myData = transformer.transform(myData, outfieldIdentities)
    print "Added Col"
    print myData
    print

    # Add column that is an average of A and C, and remove original B
    averageACnoB = ['A', 'C', 'D', 'B2', 
                    ('Avg(A, C)', ('Average', {'fieldNames': ['A', 'C']}))]
    myData = transformer.transform(myData, averageACnoB)
    print "Averaged A and C, Removed Original B"
    print myData
    print

