package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;

import Util.Pair;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * NestedAtomic Class The class is used to store the keys for each of the fields
 * that would potentially map together on both sides of the communication. The
 * keys help the values to be set in the target message fields.
 * 
 * @author tirthmehta
 */

public class NestedAtomic extends FieldData
{

    public static final String NESTED_ATOMIC_INDICES_KEY = "nestedAtomicIndices";

    private List<Pair<Class<?>, String>> indices;

    // CONSTRUCTORS
    public NestedAtomic(List<Pair<Class<?>, String>> indices)
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

    public List<Pair<Class<?>, String>> getIndices()
    {
	return indices;
    }

    public void setIndices(List<Pair<Class<?>, String>> indices)
    {
	this.indices = indices;
    }

    public void addIndex(Class<?> clazz, String index)
    {
	if (this.indices == null)
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
	
	List<Pair<String, String>> indicesWithClassesAsStrings = (List<Pair<String,String>>) SerializationConvenience.untokenizeObject(token.getItem(NESTED_ATOMIC_INDICES_KEY));
	this.indices = new ArrayList<>();
	
	for (Pair<String, String> indexWithClassAsString : indicesWithClassesAsStrings)
	{
	    if(indexWithClassAsString.getFirst() != null)
	    {
		try
		{
		    Class<?> clazz = Class.forName(indexWithClassAsString.getFirst());
		    Pair<Class<?>, String> index = new Pair<Class<?>, String>(clazz, indexWithClassAsString.getSecond());
		    this.indices.add(index);
		} catch (ClassNotFoundException e)
		{
		    //If we can't parse the class then skip this index.
		    e.printStackTrace();
		    continue;
		}	
	    }
	}
	
    }

    @Override
    public StorageToken saveToToken()
    {
	StorageToken result = super.saveToToken();

	List<Pair<String, String>> classesAsStrings = new ArrayList<>();

	for (Pair<Class<?>, String> index : this.indices)
	{
	    String classAsString = index.getFirst().getName();
	    Pair<String, String> indexWithClassAsString = new Pair<>(classAsString, index.getSecond());
	    classesAsStrings.add(indexWithClassAsString);
	}

	result.setItem(NESTED_ATOMIC_INDICES_KEY, SerializationConvenience.tokenizeObject(classesAsStrings));
	return result;
    }

}
