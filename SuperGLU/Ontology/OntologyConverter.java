package Ontology;

import java.util.List;

import Ontology.Mappings.MessageMap;

public class OntologyConverter
{
    static MessageMap correctMap = null;

    private List<MessageMap> messageMaps;

    public OntologyConverter()
    {
	messageMaps = null;
    }
    

    /**
     * Test code makes a mapping for scenarioName; Mapping is variable testMap;
     * x = [testMap,]
     * 
     * @param x
     */
    public OntologyConverter(List<MessageMap> x)
    {
	messageMaps = x;
    }

}
