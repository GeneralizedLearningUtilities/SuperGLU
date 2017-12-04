package edu.usc.ict.superglu.ontology.converters;

import org.junit.Assert;
import org.junit.Test;

public class XMLActWrappedTest
{

	@Test
    public void testConvert()
    {
	DataConverter converter = new XMLActWrapped("Speech");
	Object result = converter.convert("testString", "penguins");
	
	result.toString();
	
	Assert.assertEquals("Brad all 0 <?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<act><participant id=\"Brad\" role=\"actor\"/><fml><turn start=\"take\" end=\"give\"/><affect type=\"netural\" target=\"addressee\"/><culture type=\"neutral\"/><personality type=\"neutral\"/></fml><bml><speech id=\"sp1\" ref=\"DummyID\" type=\"application/ssml+xml\">penguins</speech></bml></act>", result.toString());
    }

}
