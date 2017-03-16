package Ontology.Converters.Tests;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.List;

import org.junit.Assert;
import org.junit.Test;

import Ontology.Converters.DataConverter;
import Ontology.Converters.XMLActWrapped;

public class XMLActWrappedTest
{

    @Test
    public void testJoin()
    {
	List<Object> input = new ArrayList<>();
	
	input.add("testString");
	
	DataConverter converter = new XMLActWrapped("Speech");
	Object result = converter.join(input);
	
	result.toString();
	
	Assert.assertEquals("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<act><participant id=\"Rachel\" role=\"actor\"/><fml><turn start=\"take\" end=\"give\"/><affect type=\"netural\" target=\"addressee\"/><culture type=\"neutral\"/><personality type=\"neutral\"/></fml><bml><speech id=\"sp1\" ref=\"DummyID\" type=\"application/ssml+xml\">testString</speech></bml></act>", result.toString());
    }

    @Test
    public void testSplit()
    {
	String xmlString = "<Speech>testString</Speech>";
	
	DataConverter converter = new XMLActWrapped("Speech");
	List<Object> result = converter.split(xmlString);
	
	Assert.assertEquals(result.get(0), "testString");
    }

}
