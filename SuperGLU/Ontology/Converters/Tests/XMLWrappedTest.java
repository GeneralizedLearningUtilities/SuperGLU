package Ontology.Converters.Tests;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.List;

import org.junit.Assert;
import org.junit.Test;

import Ontology.Converters.DataConverter;
import Ontology.Converters.XMLWrapped;

public class XMLWrappedTest
{

    @Test
    public void testJoin()
    {
	List<Object> input = new ArrayList<>();
	
	input.add("testString");
	
	DataConverter converter = new XMLWrapped("Speech");
	Object result = converter.join(input);
	
	result.toString();
	
	Assert.assertEquals("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Speech>testString</Speech>", result.toString());
    }

    @Test
    public void testSplit()
    {
	String xmlString = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Speech>testString</Speech>";
	
	DataConverter converter = new XMLWrapped("Speech");
	List<Object> result = converter.split(xmlString);
	
	Assert.assertEquals(result.get(0), "testString");
    }

}
