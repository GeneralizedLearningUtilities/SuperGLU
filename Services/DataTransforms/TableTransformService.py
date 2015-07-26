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
        super(TableTransformFunction, self).__init__(anId, gateway, authenticator)
        self._functions = dict([(x.getName(), x) for x in functions])
        if IdentityTransform.DEFAULT_NAME not in self._functions:
            self._functions[IdentityTransform.DEFAULT_NAME] = IdentityTransform()

    def transform(self, table, outputFields=None, **kwds):
        # Properly format output fields
        if outputFields is None: outputFields = []
        for i, f in enumerate(outputFields):
            if isinstance(f, basestring):
                outputFields[i] = (f, None)
        # Early returns: No transforms, other than adding header
        if len(table) == 0 or outputFields is None:
            return [[name for name, functs in outputFields]]
        # If no function declared, assume an identity with col of same name
        for name, data in outputFields:
            if data is None:
                outputFields[name] = (IdentityTransform.DEFAULT_NAME,
                                      {'fieldName' : name})
            elif outputFields[name][1] is None:
                outputFields[name] = (outputFields[name][0], {})
        header = table[0]
        newTable = [[name for name, functs in outputFields]]
        for name, data in outputFields:
            functName, params = data
            for i, row in enumerate(table):
                # TODO: Resume here
                pass
        


class TableTransform(NamedSerializable):
    def __init__(self, id=None, name=None):
        super(TableTransformFunction, self).__init__(id, name)

    def __call__(self, rowDict, rowNum, header, matrix, **kwds):
        raise NotImplementedError

    
class IdentityTransform(TableTransform):
    DEFAULT_NAME = 'Identity'
    def __init__(self, id=None, name=DEFAULT_NAME):
        super(TableTransformFunction, self).__init__(id, name)
        
    def __call__(self, rowDict, rowNum, header, matrix, **kwds):
        raise NotImplementedError 
