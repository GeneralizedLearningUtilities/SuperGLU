package Ontology.Converters;

import java.util.List;

import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * This converter will extract a single String from a List<String>
 * @author auerbach
 *
 */
public class GetElementFromStringList extends Serializable implements DataConverter
{
    public static final String INDEX_KEY = "index";

    
    /**
     * the index of the desired element in the list.
     */
    protected int index;

    
    
    public GetElementFromStringList()
    {
	super();
	this.index = -1;
    }
    
    
    public GetElementFromStringList(int index)
    {
	super();
	this.index = index;
    }

    
    //Getters/Setters
    public int getIndex()
    {
	return this.index;
    }

    public void setDelimiter(int index)
    {
	this.index = index;
    }

    
    // DataConverter Interface
    @Override
    public boolean isApplicable(Object input)
    {
	return input instanceof List;
    }

    /**
     * inputType: List<String>
     * outputType: String
     */
    @Override
    public Object convert(Object input, Object context)
    {
	List<String> inputAsList = (List) input;
	
	String result = "";
	
	try
	{
	    result = inputAsList.get(this.index);
	} catch (ArrayIndexOutOfBoundsException e)
	{
	    String errorMessage = "Data Converter failed to access specified index of the list: input= " + input.toString();
	    
	    if(context != null)
		errorMessage += "| context= " + context.toString();
	    
	    logger.error(errorMessage, e);
	}
	
	return result;
    }

    
    // Equality Operators
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;
	
	if (!(otherObject instanceof GetElementFromStringList))
	    return false;
	
	GetElementFromStringList other = (GetElementFromStringList) otherObject;
	
	if(this.index != other.index)
	    return false;
	
	
	return true;	
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	result = result * arbitraryPrimeNumber + Integer.hashCode(index);
	
	return result;
    }

    
    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);

	this.index = (int) SerializationConvenience.untokenizeObject(token.getItem(INDEX_KEY));
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();

	result.setItem(INDEX_KEY, SerializationConvenience.tokenizeObject(this.index));
	return result;
    }

}
