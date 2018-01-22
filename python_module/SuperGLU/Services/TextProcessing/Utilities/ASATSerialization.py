import lxml.builder
import lxml.etree


class ASATSerializable(object):
    """ A mixin for a class that can be serialized to match ASAT """
    ELEMENT_CLASS = lxml.etree.Element

    def __init__(self):
        super(ASATSerializable, self).__init__()

    # Generic LXML Make/Load Elements
    def _saveToXMLElement(self, name):
        return self.ELEMENT_CLASS(name)

    def _initializeFromXMLElement(self, node):
        pass

    # Override to Determine Data Load/Save
    def getASATData(self, name):
        return self._saveToXMLElement(name)

    def loadFromASATData(self, node):
        self._initializeFromXMLElement(node)

    @classmethod
    def createFromASATData(cls, node):
        x = cls()
        x.loadFromASATData(node)
        return x

    # To/From XML Strings
    def outputASATDataStr(self, name):
        node = self.getASATData(name)
        return lxml.etree.tostring(node)

    def loadFromASATDataStr(self, xml):
        node = lxml.etree.fromstring(xml)
        self.loadFromASATData(node)

    @classmethod
    def createFromASATDataStr(cls, xml):
        x = cls()
        x.loadFromASATDataStr(xml)
        return x

    # Helper Functions for Common Special Cases
    def _makeASATDataSeq(self, name, itemName, sequence, idTag=None):
        seq = [s.getASATData(itemName) for s in sequence]
        if idTag is not None:
            for i, x in enumerate(seq):
                x.attrib[idTag] = unicode(i+1)
        if name is None:
            return seq
        else:
            x = self.ELEMENT_CLASS(name)
            x.extend(seq)
            return x

    def _loadASATDataSeq(self, itemClass, node, idTag=None, name=None):
        """
        Load a sequence of ASAT data from XML nodes to Python
        @param itemClass: The class to create from this data
        @type itemClass: AutoTutorInterpreter.Utilities.ASATSerializable.ASATSerializable
        @param node: The node to draw data from.  Its children will be loaded.
        @type type: lxml.etree.Element
        @param idTag: Tag in the data to look for, which determines ordering
        @type idTag: str
        """
        if name is None:
            nodes = [node]
        else:
            name = name.lower()
            nodes = [x for x in node if isinstance(x.tag, basestring) and name == x.tag.lower()]
        fullSeq = []
        for n in nodes:
            if idTag is None:
                seq = [itemClass.createFromASATData(s) for s in n
                       if isinstance(s.tag, basestring)]
            else:
                def getId(x, default):
                    if idTag in x.attrib:
                        return x.attrib[idTag]
                    else:
                        return str(default)
                seq = [(int(getId(s, i)), itemClass.createFromASATData(s)) for i, s in enumerate(n)
                       if isinstance(s.tag, basestring)]
                seq.sort()
                seq = [obj for (i, obj) in seq]
            fullSeq.extend(seq)
        return fullSeq

