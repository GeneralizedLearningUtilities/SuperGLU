package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;

import Util.Serializable;


public class SpaceSeparation extends Serializable implements DataConverter
{
    
    public SpaceSeparation()
    {
	super();
    }

    @Override
    public Object join(List<Object> inFields)
    {
	String result = null;
	
	for(Object inField : inFields)
	{
	    if(result == null)
	    {
		if(inField == null)
		    result = "";
		else
		    result = inField.toString();
	    }
	    else if (inField == null)
		result += " ";
	    else
		result += " " + inField.toString();
	}
	
	return result;
    }

    @Override
    public List<Object> split(Object inField)
    {
	String inFieldAsString = (String)inField;
	String[] tokenizedString = inFieldAsString.split(" ");
	List<Object> result = new ArrayList<>();
	
	for(String subString : tokenizedString)
	{
	    result.add(subString);
	}
	
	return result;
    }

}
