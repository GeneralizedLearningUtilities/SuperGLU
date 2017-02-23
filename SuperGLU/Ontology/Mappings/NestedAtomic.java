package Ontology.Mappings;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import Util.Pair;
import Util.Serializable;
import Util.SerializationConvenience;
import Util.StorageToken;

/**
 * NestedAtomic Class The class is used to store the keys for each of the fields
 * that would potentially map together on both sides of the communication. The
 * keys help the values to be set in the target message fields.
 * 
 * @author auerbach
 * @author tirthmehta
 * 
 */

public class NestedAtomic extends Serializable implements FieldData
{

    public static final String NESTED_ATOMIC_INDICES_KEY = "nestedAtomicIndices";

    private static final Logger log = LoggerFactory.getLogger(NestedAtomic.class);

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

	List<Pair<String, String>> indicesWithClassesAsStrings = (List<Pair<String, String>>) SerializationConvenience.untokenizeObject(token.getItem(NESTED_ATOMIC_INDICES_KEY));
	this.indices = new ArrayList<>();

	for (Pair<String, String> indexWithClassAsString : indicesWithClassesAsStrings)
	{
	    if (indexWithClassAsString.getFirst() != null)
	    {
		try
		{
		    Class<?> clazz = Class.forName(indexWithClassAsString.getFirst());
		    Pair<Class<?>, String> index = new Pair<Class<?>, String>(clazz, indexWithClassAsString.getSecond());
		    this.indices.add(index);
		} catch (ClassNotFoundException e)
		{
		    // If we can't parse the class then skip this index.
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

    @Override
    public Object retrieveFieldData(StorageToken msg)
    {
	Object currentContainer = msg;

	for (Pair<Class<?>, String> intermediateField : this.indices)
	{
	    // Object does not exist, return null
	    if (currentContainer == null)
		return null;

	    if (currentContainer instanceof StorageToken)
	    {
		StorageToken containerAsStorageToken = (StorageToken) currentContainer;
		currentContainer = containerAsStorageToken.getItem(intermediateField.getSecond());
	    } else if (currentContainer instanceof List<?>)
	    {
		List<?> containerAsList = (List<?>) currentContainer;
		int listIndex = Integer.parseInt(intermediateField.getSecond());
		currentContainer = containerAsList.get(listIndex);
	    } else if (currentContainer instanceof Map<?, ?>)
	    {// This code will currently assume that the Map has a key of
	     // Strings for the moment.
		Map<String, Object> containerAsMap = (Map<String, Object>) currentContainer;
		currentContainer = containerAsMap.get(intermediateField.getSecond());
	    } else
	    {
		// TODO: return null or throw exception?
		String warning = "index:" + intermediateField.getSecond() + " does not exist in StorageContainer: " + currentContainer.toString();
		NestedAtomic.log.warn(warning);
		throw new RuntimeException(warning);
	    }
	}

	Object result = SerializationConvenience.untokenizeObject(currentContainer);
	return result;
    }

    private Object createNextContainer(Class<?> clazz)
    {
	try
	{
	    Object nextContainerUntokenized = clazz.newInstance();
	    Object result = SerializationConvenience.tokenizeObject(nextContainerUntokenized);
	    return result;
	} catch (InstantiationException | IllegalAccessException e)
	{
	    // TODO Auto-generated catch block
	    e.printStackTrace();
	    log.warn("failed to create object of type: " + clazz.getName());
	    throw new RuntimeException(e);
	}

    }

    @Override
    public void storeData(StorageToken msg, Object data)
    {
	Object currentContainer = msg;

	// if the message is null just stop
	if (msg == null)
	{
	    log.warn("attempted to store data to a null object, failing gracefully");
	    return;
	}
	// Tokenize the object (probably not necessary, but good to make sure)

	Object tokenizedData = SerializationConvenience.tokenizeObject(data);

	// We only want to drill down to the second to last item in the list.
	for (Pair<Class<?>, String> intermediateContainerData : this.indices.subList(0, this.indices.size() - 1))
	{
	    Object nextContainer;
	    // Object does not exist. We'll have to create it.
	    if (currentContainer instanceof StorageToken)
	    {
		StorageToken containerAsStorageToken = (StorageToken) currentContainer;
		nextContainer = containerAsStorageToken.getItem(intermediateContainerData.getSecond());

		if (nextContainer == null)
		{
		    Class<?> clazz = intermediateContainerData.getFirst();
		    nextContainer = createNextContainer(clazz);
		    containerAsStorageToken.setItem(intermediateContainerData.getSecond(), nextContainer);
		}

	    } else if (currentContainer instanceof List<?>)
	    {
		List<Object> containerAsList = (List<Object>) currentContainer;
		int listIndex = Integer.parseInt(intermediateContainerData.getSecond());
		nextContainer = containerAsList.get(listIndex);

		if (nextContainer == null)
		{
		    Class<?> clazz = intermediateContainerData.getFirst();
		    nextContainer = createNextContainer(clazz);
		    containerAsList.add(listIndex, nextContainer);
		}

	    } else if (currentContainer instanceof Map<?, ?>)
	    {// This code will currently assume that the Map has a key of
	     // Strings for the moment.
		Map<String, Object> containerAsMap = (Map<String, Object>) currentContainer;
		nextContainer = containerAsMap.get(intermediateContainerData.getSecond());

		if (nextContainer == null)
		{
		    Class<?> clazz = intermediateContainerData.getFirst();
		    nextContainer = createNextContainer(clazz);
		    containerAsMap.put(intermediateContainerData.getSecond(), nextContainer);
		}

	    } else
	    {// We've got a primitive. We'll have to
	     // TODO: Adjust this so that it handles things properly. Can't
	     // think right now.
		String warning = "index:" + intermediateContainerData.getSecond() + " already exists as a different type in StorageContainer: " + currentContainer.toString();
		NestedAtomic.log.warn(warning);

		nextContainer = this.createNextContainer(intermediateContainerData.getFirst());

		if (currentContainer instanceof StorageToken)
		    ((StorageToken) currentContainer).setItem(intermediateContainerData.getSecond(), nextContainer);
		else if (currentContainer instanceof List<?>)
		    ((List) currentContainer).add(Integer.parseInt(intermediateContainerData.getSecond()), nextContainer);
		else if (currentContainer instanceof Map<?, ?>)
		    ((Map) currentContainer).put(intermediateContainerData.getSecond(), nextContainer);

	    }

	    currentContainer = nextContainer;
	}

	String fieldName = this.indices.get(this.indices.size() - 1).getSecond();

	if (fieldName != null)
	{
	    if (currentContainer instanceof StorageToken)
		((StorageToken) currentContainer).setItem(fieldName, tokenizedData);
	    else if (currentContainer instanceof List<?>)
	    {
		int index = Integer.parseInt(fieldName);
		if(((List) currentContainer).size() < index)
		    ((List) currentContainer).add(index, tokenizedData);
		else
		    ((List) currentContainer).set(index, tokenizedData);
	    }
	    else if (currentContainer instanceof Map<?, ?>)
		((Map) currentContainer).put(fieldName, tokenizedData);
	}
    }

}
