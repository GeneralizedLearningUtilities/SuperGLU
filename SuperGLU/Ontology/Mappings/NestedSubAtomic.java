package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;
import Util.Pair;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * This class represents all the information to retrieve data from part of a field
 * @author auerbach
 *
 */
public class NestedSubAtomic extends NestedAtomic
{

    public static String CONVERTER_KEY = "converter";
    public static String INDEX_KEY = "index";
    
    
    private DataConverter converter;
    private int index;
    
    
    public NestedSubAtomic(List<Pair<Class<?>, String>> indices, DataConverter converter, int index)
    {
	super(indices);
	this.converter = converter;
	this.index = index;
    }

    public NestedSubAtomic()
    {
	super();
	this.converter = null;
	this.index = 0;
    }

    
    //Accessors
    public DataConverter getConverter()
    {
        return converter;
    }

    public void setConverter(DataConverter converter)
    {
        this.converter = converter;
    }

    public int getIndex()
    {
        return index;
    }

    public void setIndex(int index)
    {
        this.index = index;
    }
    
    
    //Equality operators
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof NestedSubAtomic))
	    return false;

	NestedSubAtomic other = (NestedSubAtomic) otherObject;

	if (!fieldIsEqual(this.converter, other.converter))
	    return false;

	return true;
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	if (this.converter != null)
	    result = result * arbitraryPrimeNumber + this.converter.hashCode();
	
	result = result * arbitraryPrimeNumber + index;

	return result;

    }
    
    
    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);

	this.converter = (DataConverter) SerializationConvenience.untokenizeObject(token.getItem(CONVERTER_KEY));
	this.index = (int) SerializationConvenience.untokenizeObject(token.getItem(INDEX_KEY));

    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();

	result.setItem(CONVERTER_KEY, SerializationConvenience.tokenizeObject(converter));
	result.setItem(INDEX_KEY, SerializationConvenience.tokenizeObject(this.index));
	return result;
    }
    
    
    
    //data storage and retrieval
    @Override
    public Object retrieveFieldData(StorageToken msg)
    {
	Object fieldData = super.retrieveFieldData(msg);
	List<Object> splitField = converter.split(fieldData);
	Object result = splitField.get(this.index);
	return result;
    }
    
    
    @Override
    public void storeData(StorageToken msg, Object data)
    {
	Object currentFieldData = super.retrieveFieldData(msg);
	
	List<Object> tokenizedObjectList;
	
	if(currentFieldData == null)
	    tokenizedObjectList = new ArrayList<>(index);
	else
	    tokenizedObjectList = converter.split(currentFieldData);
	
	while(tokenizedObjectList.size() < index + 1)
	    tokenizedObjectList.add(null);
	
	tokenizedObjectList.set(index, data);
	
	Object newFieldData = converter.join(tokenizedObjectList);
	
	super.storeData(msg, newFieldData);
    }
    
    
}
