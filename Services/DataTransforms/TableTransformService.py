"""
This service converts one table into another table,
by changing the headings (e.g., add, remove, re-sort),
and possibly adding calculated fields to the table.
"""
from SuperGLU.Core.MessagingGateway import BaseService
from SuperGLU.Services.DataTransforms.TableTransforms import TableTransformer

class TableTransformService(BaseService, TableTransformer):
    TABLE_KEY = 'table'
    OUTPUT_FIELDS_KEY = 'outputFields'
    
    def __init__(self, functions=None, anId=None, gateway=None, authenticator=None):
        """
        Receive a list of TableTransform instances,
        These will be turned into a map of the function name to
        the instance, so that these can be used to evaluate data.
        """
        BaseService.__init__(self, anId, gateway, authenticator)
        TableTransformer.__init__(self, functions)

    def transformJSONObj(self, jsonObj):
        jsonObj[self.TABLE_KEY] = self.transform(**jsonObj)
        return jsonObj
        

if __name__ == '__main__':
    import json
    from SuperGLU.Services.DataTransforms.TableTransforms import  AverageFieldsTransform
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
    myDataJSON = json.dumps({'table' : myData, 'outputFields' : sortColsFunct,
                             'miscDoNothing' : None})
    myDataJSONObj = json.loads(myDataJSON)
    myData = transformer.transformJSONObj(myDataJSONObj)
    print "Rearranged"
    print myData['table']
    print

    # Add identity columns that duplicate rows B and D
    outfieldIdentities = ['A', 'B', 'C', 'D',
                          ('B2', 'Identity', {'fieldName':'B'})]
    myDataJSONObj['outputFields'] = outfieldIdentities
    myData = transformer.transformJSONObj(myDataJSONObj)
    print "Added Col"
    print myData['table']
    print

    # Add column that is an average of A and C, and remove original B
    averageACnoB = ['A', 'C', 'D', 'B2', 
                    ('Avg(A, C)', 'Average', {'fieldNames': ['A', 'C']})]
    myDataJSONObj['outputFields'] = averageACnoB
    myData = transformer.transformJSONObj(myDataJSONObj)
    print "Averaged A and C, Removed Original B"
    print myData['table']
    print


