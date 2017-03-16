package Ontology.Converters;

import java.util.ArrayList;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.DocumentFactory;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * This converter will wrap a field partial in an xml element with the specified name
 * @author auerbach
 *
 */
public class XMLActWrapped extends Serializable implements DataConverter
{
    
    public static final String ELEMENT_NAME_KEY = "elementName";
    
    
    protected String elementName;
    
    
    public XMLActWrapped()
    {
	this.elementName = "defaultName";
    }
    
    
    public XMLActWrapped(String elementName)
    {
	this.elementName = elementName;
    }
    

    public String getElementName()
    {
        return elementName;
    }


    public void setElementName(String elementName)
    {
        this.elementName = elementName;
    }


    @Override
    public Object join(List<Object> inFields)
    {
	/*
	<act>
		<participant id="Rachel" role="actor" />
		<fml>
			<turn start="take" end="give" />
			<affect type="neutral" target="addressee"></affect>
			<culture type="neutral"></culture>
			<personality type="neutral"></personality>
		</fml>
		<bml>
			<speech id="sp1" ref="DummyID" type="application/ssml+xml">Hello I am a virtual human</speech>
		</bml>
	</act>
	*/
	DocumentFactory docFactory = DocumentFactory.getInstance();
	
	Document result = docFactory.createDocument();
	
	Element actElement = docFactory.createElement("act");
	
	Element participantElement = docFactory.createElement("participant");
	participantElement.addAttribute("id", "Rachel");
	participantElement.addAttribute("role", "actor");
	actElement.add(participantElement);
	
	Element fmlElement = docFactory.createElement("fml");
	
	Element turnElement = docFactory.createElement("turn");
	turnElement.addAttribute("start", "take");
	turnElement.addAttribute("end", "give");
	fmlElement.add(turnElement);
	
	Element affectElement = docFactory.createElement("affect");
	affectElement.addAttribute("type", "netural");
	affectElement.addAttribute("target", "addressee");
	fmlElement.add(affectElement);
	
	Element cultureElement = docFactory.createElement("culture");
	cultureElement.addAttribute("type", "neutral");
	fmlElement.add(cultureElement);
	
	Element personalityElement = docFactory.createElement("personality");
	personalityElement.addAttribute("type", "neutral");
	fmlElement.add(personalityElement);
	
	actElement.add(fmlElement);
	
	Element bmlElement = docFactory.createElement("bml");
	Element speechElement = docFactory.createElement("speech");
	speechElement.addAttribute("id", "sp1");
	speechElement.addAttribute("ref", "DummyID");
	speechElement.addAttribute("type", "application/ssml+xml");
	speechElement.addText((String)inFields.get(0));
	bmlElement.add(speechElement);
	
	actElement.add(bmlElement);
	
	result.add(actElement);
	
	return result.asXML();
    }

    @Override
    public List<Object> split(Object inField)
    {
	List<Object> result = new ArrayList<>();
	try
	{
	    Document doc = DocumentHelper.parseText((String) inField);
	    Element element = doc.getRootElement();
	    String text = element.getText();
	    
	    result.add(text);
	
	} catch (DocumentException e)
	{
	    // TODO Auto-generated catch block
	    e.printStackTrace();
	}
	
	return result;
    }

    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	
	this.elementName = (String)SerializationConvenience.untokenizeObject(token.getItem(ELEMENT_NAME_KEY, true, "defaultName"));
    }

    @Override
    public StorageToken saveToToken()
    {
	return super.saveToToken();
	
    }
    
    
    

}
