package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;

/**
 * NestedAtomic  Class
 * The class is used to store the keys for each of the fields that would potentially map together on both sides of the 
 * communication. The keys help the values to be set in the target message fields.
 * @author tirthmehta
 */
import Util.SerializationConvenience;
import Util.StorageToken;

public class NestedAtomic extends FieldData
{

    public static final String NESTED_ATOMIC_INDICES_KEY = "nestedAtomicIndices";
    
    private List<String> indices;
   

    // CONSTRUCTORS
    public NestedAtomic(List<String> index)
    {
	if (index == null)
	    indices = null;
	else
	{
	    indices = new ArrayList<>();
	    for (String in:index)
	    {
		indices.add(in);
	    }
	}

    }
   

    public NestedAtomic()
    {
	this.indices = null;
    }

    // GETTER AND SETTER METHODS
  
    public List<String> getIndex()
    {
	return indices;
    }

    public void setIndex(List<String> index)
    {
	if (index != null)
	{
	    indices = new ArrayList<>();
	    for (String in:index)
	    {
		indices.add(in);
	    }
	}
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject)
    {
	if (!super.equals(otherObject))
	    return false;

	if (!(otherObject instanceof NestedAtomic))
	    return false;

	NestedAtomic other = (NestedAtomic) otherObject;

	if (!fieldIsEqual(this.indices, other.indices))
	    return false;
	

	return true;
    }

    @Override
    public int hashCode()
    {
	int result = super.hashCode();
	int arbitraryPrimeNumber = 23;

	if (this.indices != null)
	    result = result * arbitraryPrimeNumber + this.indices.hashCode();
	
	return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token)
    {
	super.initializeFromToken(token);
	this.indices = (List<String>) SerializationConvenience.untokenizeObject(token.getItem(NESTED_ATOMIC_INDICES_KEY));
	
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(NESTED_ATOMIC_INDICES_KEY, SerializationConvenience.tokenizeObject(this.indices));
	return result;
    }

}
