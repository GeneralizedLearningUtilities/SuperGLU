package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;

import Util.Pair;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * NestedAtomic  Class
 * The class is used to store the keys for each of the fields that would potentially map together on both sides of the 
 * communication. The keys help the values to be set in the target message fields.
 * @author tirthmehta
 */


public class NestedAtomic extends FieldData
{

    public static final String NESTED_ATOMIC_INDICES_KEY = "nestedAtomicIndices";
    
    private List<Pair<Class<?>,String>> indices;
   

    // CONSTRUCTORS
    public NestedAtomic(List<Pair<Class<?>,String>> indices)
    {
	this.indices = indices;
    }
    
    
    public NestedAtomic(Class<?> clazz, String index)
    {
	this.indices = new ArrayList<>();
	this.addIndex(clazz, index);
    }
   

    public NestedAtomic()
    {
	this.indices = null;
    }

    // GETTER AND SETTER METHODS
  
    public List<Pair<Class<?>,String>> getIndices()
    {
	return indices;
    }

    public void setIndices(List<Pair<Class<?>, String>> indices)
    {
	this.indices = indices;
    }
    
    public void addIndex(Class<?> clazz, String index)
    {
	if(this.indices == null)
	    this.indices = new ArrayList<>();
	
	
	this.indices.add(new Pair<Class<?>, String>(clazz, index));
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
	this.indices = (List<Pair<Class<?>,String>>) SerializationConvenience.untokenizeObject(token.getItem(NESTED_ATOMIC_INDICES_KEY));
	
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();
	result.setItem(NESTED_ATOMIC_INDICES_KEY, SerializationConvenience.tokenizeObject(this.indices));
	return result;
    }

}
