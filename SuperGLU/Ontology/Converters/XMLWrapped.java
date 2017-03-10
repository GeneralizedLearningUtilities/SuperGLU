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
public class XMLWrapped extends Serializable implements DataConverter
{
    
    public static final String ELEMENT_NAME_KEY = "elementName";
    
    
    protected String elementName;
    
    
    public XMLWrapped()
    {
	this.elementName = "defaultName";
    }
    
    
    public XMLWrapped(String elementName)
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
	Document doc = DocumentFactory.getInstance().createDocument();
	Element element = DocumentFactory.getInstance().createElement(elementName);
	element.addText((String)inFields.get(0));
	doc.add(element);
	return doc.asXML();
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
