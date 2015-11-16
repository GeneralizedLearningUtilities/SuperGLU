from gludb.simple import DBObject, Field, Index
from gludb.config import default_database, Database

@DBObject(table_name='IncomingMessages')
class IncomingMessage(object):
    rawMessage=Field('rawMessage')
    